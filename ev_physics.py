"""
EV Powertrain Simulation Engine
Physics models for Electric Vehicle Digital Twin:
- Longitudinal Vehicle Dynamics (Aerodynamic, Rolling, Gradient, Acceleration resistance)
- Electric Motor Characteristics (PMSM, Induction, BLDC, Axial Flux)
- Motor Efficiency Map modeling (Copper, Iron, Windage, and Stray losses)
- Transmission Modeling (Single-Speed, 2-Speed Dual Ratio, CVT)
- Dynamic Tests: 0-100 km/h Sprint, Gradeability vs Speed, Energy Consumption (WLTP/Highway)
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

# Physical constants
AIR_DENSITY_RHO = 1.225  # kg/m^3 at sea level, 15°C
GRAVITY_G = 9.80665      # m/s^2

@dataclass
class VehicleParams:
    name: str = "Custom EV"
    mass_kg: float = 1800.0            # Curb mass + driver (kg)
    frontal_area_m2: float = 2.25      # Frontal area (m^2)
    drag_coefficient_cd: float = 0.26  # Aerodynamic drag coefficient
    rolling_resistance_cr: float = 0.010 # Rolling resistance coefficient
    wheel_radius_m: float = 0.33       # Dynamic tire radius (m)
    drivetrain_efficiency: float = 0.94 # Mechanical transmission efficiency
    auxiliary_power_w: float = 400.0   # AC, electronics, infotainment baseline (W)
    battery_capacity_kwh: float = 65.0 # Battery pack capacity (kWh)
    rotational_inertia_factor: float = 1.05 # Rotational inertia correction (1 + delta)

@dataclass
class MotorParams:
    motor_type: str = "PMSM (Permanent Magnet)"
    rated_power_kw: float = 160.0       # Rated maximum continuous/peak power (kW)
    peak_torque_nm: float = 330.0       # Peak stall/low-speed torque (Nm)
    base_speed_rpm: float = 4600.0      # Speed at which motor transitions from constant torque to constant power
    max_speed_rpm: float = 16000.0      # Max mechanical operating speed (rpm)
    peak_efficiency: float = 0.965      # Maximum achievable efficiency (e.g. 96.5%)

@dataclass
class TransmissionParams:
    gearbox_type: str = "Single-Speed Reduction Gearbox" # "Single-Speed Reduction Gearbox" or "2-Speed Automatic"
    gear_ratio_1: float = 8.8           # Primary reduction ratio
    gear_ratio_2: float = 5.2           # High gear ratio (if 2-speed)
    shift_speed_kmh: float = 75.0       # Shift point for 2-speed gearbox
    shift_duration_s: float = 0.25      # Interruption time during gear change

class EVSimulationEngine:
    def __init__(self, vehicle: VehicleParams, motor: MotorParams, transmission: TransmissionParams):
        self.veh = vehicle
        self.motor = motor
        self.trans = transmission

        # Re-calibrate base speed if not matched to power & torque
        calculated_base_rpm = (self.motor.rated_power_kw * 1000.0 * 9.549297) / max(1.0, self.motor.peak_torque_nm)
        if self.motor.base_speed_rpm <= 0 or abs(self.motor.base_speed_rpm - calculated_base_rpm) > 1500:
            self.motor.base_speed_rpm = min(calculated_base_rpm, self.motor.max_speed_rpm * 0.6)

    def get_motor_torque_limit(self, speed_rpm: float) -> float:
        """Calculates maximum available motor torque at a given RPM."""
        if speed_rpm <= 0:
            return self.motor.peak_torque_nm
        if speed_rpm <= self.motor.base_speed_rpm:
            return self.motor.peak_torque_nm
        elif speed_rpm <= self.motor.max_speed_rpm:
            # Constant power region: T = P / omega
            omega = (speed_rpm * 2.0 * np.pi) / 60.0
            return (self.motor.rated_power_kw * 1000.0) / omega
        else:
            return 0.0

    def get_active_gear_ratio(self, vehicle_speed_kmh: float) -> float:
        """Determines active gear ratio based on current speed."""
        if self.trans.gearbox_type == "2-Speed Automatic":
            if vehicle_speed_kmh >= self.trans.shift_speed_kmh:
                return self.trans.gear_ratio_2
            return self.trans.gear_ratio_1
        return self.trans.gear_ratio_1

    def motor_rpm_from_vehicle_speed(self, speed_kmh: float, gear_ratio: Optional[float] = None) -> float:
        """Converts vehicle speed (km/h) to electric motor RPM."""
        speed_ms = speed_kmh / 3.6
        if gear_ratio is None:
            gear_ratio = self.get_active_gear_ratio(speed_kmh)
        wheel_omega = speed_ms / self.veh.wheel_radius_m
        motor_omega = wheel_omega * gear_ratio
        motor_rpm = (motor_omega * 60.0) / (2.0 * np.pi)
        return motor_rpm

    def vehicle_speed_from_motor_rpm(self, motor_rpm: float, gear_ratio: Optional[float] = None) -> float:
        """Converts motor RPM to vehicle speed (km/h)."""
        if gear_ratio is None:
            gear_ratio = self.trans.gear_ratio_1
        motor_omega = (motor_rpm * 2.0 * np.pi) / 60.0
        wheel_omega = motor_omega / gear_ratio
        speed_ms = wheel_omega * self.veh.wheel_radius_m
        return speed_ms * 3.6

    def calculate_motor_efficiency(self, torque_nm: float, speed_rpm: float) -> float:
        """
        Analytical/empirical motor loss model:
        Losses = k_c * T^2 (copper) + k_i * omega (iron) + k_w * omega^3 (windage) + C (stray)
        Returns efficiency between 0.60 and peak_efficiency.
        """
        torque = abs(torque_nm)
        if torque < 1e-3 or speed_rpm < 10.0:
            return 0.70

        omega = (speed_rpm * 2.0 * np.pi) / 60.0
        mech_power = torque * omega  # Watts

        # Loss coefficients scaled to motor size
        p_rated_w = self.motor.rated_power_kw * 1000.0
        t_rated = self.motor.peak_torque_nm
        omega_max = (self.motor.max_speed_rpm * 2.0 * np.pi) / 60.0

        # Fractional losses at full load
        kc = 0.025 * (p_rated_w / (t_rated**2))
        ki = 0.015 * (p_rated_w / omega_max)
        kw = 0.005 * (p_rated_w / (omega_max**3))
        c_stray = 0.008 * p_rated_w

        p_loss = (kc * (torque**2)) + (ki * omega) + (kw * (omega**3)) + c_stray
        total_elec_power = mech_power + p_loss
        eff = mech_power / max(total_elec_power, 1.0)
        
        # Scale to match peak efficiency calibration
        eff = min(self.motor.peak_efficiency, max(0.60, eff * 1.02))
        return float(eff)

    def generate_efficiency_map(self, n_speed_points: int = 40, n_torque_points: int = 40) -> Dict:
        """
        Generates 2D and 3D data for the Motor Efficiency Map (Contour and 3D Surface).
        Matches MATLAB Powertrain Blockset visual representation.
        """
        speeds_rpm = np.linspace(100, self.motor.max_speed_rpm, n_speed_points)
        torques_nm = np.linspace(5, self.motor.peak_torque_nm, n_torque_points)

        speed_grid, torque_grid = np.meshgrid(speeds_rpm, torques_nm)
        efficiency_grid = np.zeros_like(speed_grid)

        for i in range(len(torques_nm)):
            for j in range(len(speeds_rpm)):
                rpm = speeds_rpm[j]
                t = torques_nm[i]
                max_t = self.get_motor_torque_limit(rpm)
                if t > max_t:
                    efficiency_grid[i, j] = np.nan
                else:
                    efficiency_grid[i, j] = self.calculate_motor_efficiency(t, rpm) * 100.0

        return {
            "speed_rpm": speeds_rpm,
            "torque_nm": torques_nm,
            "efficiency_grid": efficiency_grid,
            "speed_grid": speed_grid,
            "torque_grid": torque_grid
        }

    def generate_torque_power_curve(self, n_points: int = 100) -> Dict:
        """
        Generates Torque & Power Characteristics curves vs Motor RPM.
        Matches MATLAB Figure 1: dual Y-axis curve.
        """
        speeds_rpm = np.linspace(0, self.motor.max_speed_rpm, n_points)
        torques_nm = []
        powers_kw = []

        for rpm in speeds_rpm:
            t = self.get_motor_torque_limit(rpm)
            torques_nm.append(t)
            omega = (rpm * 2.0 * np.pi) / 60.0
            power_kw = (t * omega) / 1000.0
            powers_kw.append(power_kw)

        return {
            "speed_rpm": speeds_rpm,
            "torque_nm": np.array(torques_nm),
            "power_kw": np.array(powers_kw),
            "base_speed_rpm": self.motor.base_speed_rpm,
            "max_speed_rpm": self.motor.max_speed_rpm,
            "peak_torque_nm": self.motor.peak_torque_nm,
            "rated_power_kw": self.motor.rated_power_kw
        }

    def calculate_road_load_forces(self, speed_kmh: float, gradient_pct: float = 0.0) -> Dict[str, float]:
        """
        Calculates all resistive forces acting on the vehicle:
        F_total = F_rolling + F_aero + F_gradient
        """
        speed_ms = speed_kmh / 3.6
        theta = np.arctan(gradient_pct / 100.0)

        f_roll = self.veh.mass_kg * GRAVITY_G * self.veh.rolling_resistance_cr * np.cos(theta)
        f_aero = 0.5 * AIR_DENSITY_RHO * self.veh.drag_coefficient_cd * self.veh.frontal_area_m2 * (speed_ms**2)
        f_grade = self.veh.mass_kg * GRAVITY_G * np.sin(theta)
        f_total = f_roll + f_aero + f_grade

        return {
            "f_roll_n": float(f_roll),
            "f_aero_n": float(f_aero),
            "f_grade_n": float(f_grade),
            "f_total_n": float(f_total)
        }

    def simulate_acceleration_sprint(self, target_speed_kmh: float = 100.0, dt: float = 0.05, max_time_s: float = 20.0) -> Dict:
        """
        Simulates 0-100 km/h acceleration sprint via numerical Euler integration.
        Outputs speed, acceleration, motor torque, power, distance over time.
        """
        time_arr = [0.0]
        speed_kmh_arr = [0.0]
        accel_arr = [0.0]
        dist_m_arr = [0.0]
        motor_rpm_arr = [0.0]
        motor_torque_arr = [self.motor.peak_torque_nm]
        motor_power_kw_arr = [0.0]
        gear_active_arr = [1]

        t = 0.0
        v = 0.0 # m/s
        s = 0.0 # m
        effective_mass = self.veh.mass_kg * self.veh.rotational_inertia_factor

        shift_delay_timer = 0.0
        current_gear = 1

        while v * 3.6 < target_speed_kmh and t < max_time_s:
            v_kmh = v * 3.6
            gear_ratio = self.get_active_gear_ratio(v_kmh)

            if self.trans.gearbox_type == "2-Speed Automatic" and v_kmh >= self.trans.shift_speed_kmh and current_gear == 1:
                # Trigger shift
                current_gear = 2
                shift_delay_timer = self.trans.shift_duration_s

            if shift_delay_timer > 0:
                shift_delay_timer -= dt
                gear_ratio = self.trans.gear_ratio_2
                t_motor = 0.0  # Torque interruption during shift
            else:
                motor_rpm = self.motor_rpm_from_vehicle_speed(v_kmh, gear_ratio)
                motor_rpm = min(motor_rpm, self.motor.max_speed_rpm)
                t_motor = self.get_motor_torque_limit(motor_rpm)

            # Available tractive force at wheel
            wheel_torque = t_motor * gear_ratio * self.veh.drivetrain_efficiency
            f_tractive = wheel_torque / self.veh.wheel_radius_m

            # Resistive road loads
            forces = self.calculate_road_load_forces(v_kmh, gradient_pct=0.0)
            f_resist = forces["f_total_n"]

            f_net = max(0.0, f_tractive - f_resist)
            a = f_net / effective_mass

            # Update state
            v += a * dt
            s += v * dt
            t += dt

            motor_rpm = self.motor_rpm_from_vehicle_speed(v * 3.6, gear_ratio)
            omega_motor = (motor_rpm * 2.0 * np.pi) / 60.0
            p_motor_kw = (t_motor * omega_motor) / 1000.0

            time_arr.append(t)
            speed_kmh_arr.append(v * 3.6)
            accel_arr.append(a)
            dist_m_arr.append(s)
            motor_rpm_arr.append(motor_rpm)
            motor_torque_arr.append(t_motor)
            motor_power_kw_arr.append(p_motor_kw)
            gear_active_arr.append(current_gear)

        zero_to_hundred_time = t if (v * 3.6 >= target_speed_kmh) else None

        return {
            "time_s": np.array(time_arr),
            "speed_kmh": np.array(speed_kmh_arr),
            "accel_ms2": np.array(accel_arr),
            "distance_m": np.array(dist_m_arr),
            "motor_rpm": np.array(motor_rpm_arr),
            "motor_torque_nm": np.array(motor_torque_arr),
            "motor_power_kw": np.array(motor_power_kw_arr),
            "gear_active": np.array(gear_active_arr),
            "zero_to_target_time_s": zero_to_hundred_time,
            "final_speed_kmh": v * 3.6
        }

    def simulate_gradeability(self, gradients: Optional[List[float]] = None) -> pd.DataFrame:
        """
        Simulates vehicle tractive reserve, max climb speed, and motor load
        across road gradients (e.g. 0% to 35%).
        """
        if gradients is None:
            gradients = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]

        results = []
        for g in gradients:
            # Check maximum continuous climb speed and tractive force
            # Wheel tractive limit at peak stall torque in 1st gear
            gear_ratio = self.trans.gear_ratio_1
            t_max_wheel = self.motor.peak_torque_nm * gear_ratio * self.veh.drivetrain_efficiency
            f_max_tractive = t_max_wheel / self.veh.wheel_radius_m

            # Road load at crawl speed (10 km/h)
            crawl_loads = self.calculate_road_load_forces(10.0, gradient_pct=g)
            f_req_crawl = crawl_loads["f_total_n"]
            can_start = f_max_tractive >= f_req_crawl

            # Find maximum steady achievable speed on gradient
            speeds_test = np.linspace(5, 160, 62)
            max_achievable_v = 0.0
            power_at_max = 0.0
            eff_at_max = 0.0

            for v_test in speeds_test:
                active_gear = self.get_active_gear_ratio(v_test)
                rpm = self.motor_rpm_from_vehicle_speed(v_test, active_gear)
                if rpm > self.motor.max_speed_rpm:
                    break
                t_limit = self.get_motor_torque_limit(rpm)
                f_avail = (t_limit * active_gear * self.veh.drivetrain_efficiency) / self.veh.wheel_radius_m
                f_req = self.calculate_road_load_forces(v_test, gradient_pct=g)["f_total_n"]

                if f_avail >= f_req:
                    max_achievable_v = v_test
                    t_req_motor = (f_req * self.veh.wheel_radius_m) / (active_gear * self.veh.drivetrain_efficiency)
                    power_at_max = (t_req_motor * (rpm * 2 * np.pi / 60)) / 1000.0
                    eff_at_max = self.calculate_motor_efficiency(t_req_motor, rpm)
                else:
                    break

            results.append({
                "Gradient (%)": g,
                "Gradient (Deg)": round(np.degrees(np.arctan(g / 100.0)), 1),
                "Hill Start Capable": "Yes" if can_start else "No",
                "Max Sustainable Speed (km/h)": round(max_achievable_v, 1),
                "Required Power at Max (kW)": round(power_at_max, 1),
                "Operating Efficiency (%)": round(eff_at_max * 100, 1) if max_achievable_v > 0 else 0.0
            })

        return pd.DataFrame(results)

    def calculate_energy_consumption(self, speed_kmh: float, distance_km: float = 100.0, gradient_pct: float = 0.0) -> Dict:
        """
        Calculates steady cruising energy consumption (kWh/100km) and estimated range.
        """
        if speed_kmh <= 0:
            return {"kwh_per_100km": 0.0, "estimated_range_km": 0.0, "power_demand_kw": 0.0}

        forces = self.calculate_road_load_forces(speed_kmh, gradient_pct=gradient_pct)
        f_total = forces["f_total_n"]
        speed_ms = speed_kmh / 3.6

        p_tractive_w = f_total * speed_ms
        gear_ratio = self.get_active_gear_ratio(speed_kmh)
        rpm = self.motor_rpm_from_vehicle_speed(speed_kmh, gear_ratio)
        t_req_motor = (f_total * self.veh.wheel_radius_m) / (gear_ratio * self.veh.drivetrain_efficiency)

        eff_motor = self.calculate_motor_efficiency(t_req_motor, rpm)
        p_elec_motor_w = (p_tractive_w / self.veh.drivetrain_efficiency) / max(0.1, eff_motor)
        p_total_elec_w = p_elec_motor_w + self.veh.auxiliary_power_w

        # Energy to travel 100 km: Time (hours) = 100 / speed_kmh
        hours_per_100km = 100.0 / speed_kmh
        kwh_per_100km = (p_total_elec_w / 1000.0) * hours_per_100km

        # Estimated range on battery capacity
        usable_battery_kwh = self.veh.battery_capacity_kwh * 0.95
        est_range_km = (usable_battery_kwh / max(0.1, kwh_per_100km)) * 100.0

        return {
            "speed_kmh": speed_kmh,
            "power_demand_kw": p_total_elec_w / 1000.0,
            "motor_rpm": rpm,
            "motor_torque_nm": t_req_motor,
            "motor_efficiency_pct": eff_motor * 100.0,
            "kwh_per_100km": kwh_per_100km,
            "estimated_range_km": est_range_km,
            "f_roll_n": forces["f_roll_n"],
            "f_aero_n": forces["f_aero_n"],
            "f_grade_n": forces["f_grade_n"]
        }

    def sweep_gear_ratios(self, ratio_range: Tuple[float, float] = (4.0, 16.0), steps: int = 15) -> pd.DataFrame:
        """
        Sweeps single-speed reduction ratios to evaluate trade-offs:
        0-100 time vs Top Speed vs 120 km/h Highway kWh/100km vs Max Gradeability %.
        """
        ratios = np.linspace(ratio_range[0], ratio_range[1], steps)
        rows = []

        # Save current state
        original_ratio = self.trans.gear_ratio_1
        original_type = self.trans.gearbox_type
        self.trans.gearbox_type = "Single-Speed Reduction Gearbox"

        for r in ratios:
            self.trans.gear_ratio_1 = r

            # 1. Top speed (governed either by motor max RPM or aerodynamic equilibrium)
            speed_at_max_rpm = self.vehicle_speed_from_motor_rpm(self.motor.max_speed_rpm, r)
            # Power limited top speed
            speeds_test = np.linspace(20, min(260, speed_at_max_rpm), 60)
            power_limited_speed = 20.0
            for sp in speeds_test:
                rpm = self.motor_rpm_from_vehicle_speed(sp, r)
                t_limit = self.get_motor_torque_limit(rpm)
                f_avail = (t_limit * r * self.veh.drivetrain_efficiency) / self.veh.wheel_radius_m
                f_req = self.calculate_road_load_forces(sp)["f_total_n"]
                if f_avail >= f_req:
                    power_limited_speed = sp
                else:
                    break

            top_speed_achieved = min(speed_at_max_rpm, power_limited_speed)

            # 2. 0-100 km/h acceleration
            sprint = self.simulate_acceleration_sprint(100.0, dt=0.08, max_time_s=18.0)
            t_accel = sprint["zero_to_target_time_s"] if sprint["zero_to_target_time_s"] is not None else 18.0

            # 3. Highway consumption at 100 km/h
            hwy = self.calculate_energy_consumption(100.0)
            kwh_100 = hwy["kwh_per_100km"]

            # 4. Max gradeability
            t_wheel_max = self.motor.peak_torque_nm * r * self.veh.drivetrain_efficiency
            f_tractive_max = t_wheel_max / self.veh.wheel_radius_m
            f_roll_crawl = self.veh.mass_kg * GRAVITY_G * self.veh.rolling_resistance_cr
            sin_theta_max = max(0.0, min(0.65, (f_tractive_max - f_roll_crawl) / (self.veh.mass_kg * GRAVITY_G)))
            gradeability_pct = np.tan(np.arcsin(sin_theta_max)) * 100.0

            rows.append({
                "Gear Ratio": round(r, 2),
                "0-100 km/h (s)": round(t_accel, 2),
                "Top Speed (km/h)": round(top_speed_achieved, 1),
                "100 km/h Energy (kWh/100km)": round(kwh_100, 2),
                "Max Gradeability (%)": round(gradeability_pct, 1),
                "RPM @ 100 km/h": round(self.motor_rpm_from_vehicle_speed(100.0, r), 0)
            })

        # Restore
        self.trans.gear_ratio_1 = original_ratio
        self.trans.gearbox_type = original_type
        return pd.DataFrame(rows)
