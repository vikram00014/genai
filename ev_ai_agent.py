"""
EV Powertrain AI Agent & Autonomous Optimizer
Powered by Groq LLM (openai/gpt-oss-120b and qwen/qwen3.8-27b).
Performs:
1. Autonomous multi-configuration parameter tuning & simulation comparison
2. Interactive Powertrain Engineering Co-Pilot
3. Technical Powertrain Sizing & MATLAB-grade engineering reports
"""

import os
import json
from typing import Dict, List, Optional, Tuple
from groq import Groq
from ev_physics import VehicleParams, MotorParams, TransmissionParams, EVSimulationEngine

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

PRIMARY_MODEL = "openai/gpt-oss-120b"
FALLBACK_MODEL = "qwen/qwen3.8-27b"

class EVAIAgent:
    def __init__(self, api_key: Optional[str] = None):
        # Check explicit parameter -> Streamlit secrets -> environment variable
        st_secret_key = None
        try:
            import streamlit as st
            if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                st_secret_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            pass

        self.api_key = api_key or st_secret_key or os.environ.get("GROQ_API_KEY", "")
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None

    def _call_llm(self, system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
        """Calls Groq with automatic fallback if primary model is unavailable."""
        if not self.client:
            return "[Groq API Key Required]: Please configure your GROQ_API_KEY in .env or Streamlit Cloud Secrets."

        models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]
        last_error = None

        for model in models_to_try:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=2048
                )
                return response.choices[0].message.content
            except Exception as e:
                last_error = e
                continue

        return f"[AI Generation Error]: {last_error}. Please check your Groq API connection."

    def run_multi_config_optimization(
        self,
        base_vehicle: VehicleParams,
        target_top_speed_kmh: float,
        target_gradeability_pct: float,
        benchmark_evs_context: str = ""
    ) -> Dict:
        """
        AI Autonomous Feature:
        1. Synthesizes 3 distinct engineering configurations (Balanced Single-Speed, Dual-Speed High Efficiency, High-Power Sport)
        2. Simulates each configuration through the EV Digital Twin physics engine
        3. Generates a comparative matrix (0-100 sprint, top speed, energy consumption, gradeability)
        4. Calls Groq to analyze which configuration performs best and provide trade-off recommendations.
        """
        # Define 3 engineering configurations
        # Config 1: Balanced Single-Speed Reduction (Optimal daily driver)
        cfg1_ratio = round((base_vehicle.wheel_radius_m * 12000.0 * 2.0 * 3.14159) / (target_top_speed_kmh * 60.0 / 3.6), 2)
        cfg1_ratio = max(7.0, min(10.5, cfg1_ratio))
        
        c1_veh = VehicleParams(
            name="Config A: Balanced Single-Speed",
            mass_kg=base_vehicle.mass_kg,
            frontal_area_m2=base_vehicle.frontal_area_m2,
            drag_coefficient_cd=base_vehicle.drag_coefficient_cd,
            wheel_radius_m=base_vehicle.wheel_radius_m,
            battery_capacity_kwh=base_vehicle.battery_capacity_kwh
        )
        c1_mot = MotorParams(
            motor_type="PMSM (Permanent Magnet)",
            rated_power_kw=max(90.0, round(base_vehicle.mass_kg * 0.08, 0)),
            peak_torque_nm=max(200.0, round(base_vehicle.mass_kg * 0.17, 0)),
            max_speed_rpm=15000.0
        )
        c1_trans = TransmissionParams(
            gearbox_type="Single-Speed Reduction Gearbox",
            gear_ratio_1=cfg1_ratio
        )

        # Config 2: 2-Speed Dual-Ratio Automatic (Porsche Taycan / Audi e-tron GT style)
        c2_veh = VehicleParams(
            name="Config B: 2-Speed High-Efficiency",
            mass_kg=base_vehicle.mass_kg + 35.0, # Additional 35kg for dual-clutch transmission
            frontal_area_m2=base_vehicle.frontal_area_m2,
            drag_coefficient_cd=base_vehicle.drag_coefficient_cd,
            wheel_radius_m=base_vehicle.wheel_radius_m,
            battery_capacity_kwh=base_vehicle.battery_capacity_kwh
        )
        c2_mot = MotorParams(
            motor_type="PMSM (Permanent Magnet)",
            rated_power_kw=c1_mot.rated_power_kw * 0.92, # Can downsize motor due to gear torque multiplication
            peak_torque_nm=c1_mot.peak_torque_nm * 0.88,
            max_speed_rpm=14500.0
        )
        c2_trans = TransmissionParams(
            gearbox_type="2-Speed Automatic",
            gear_ratio_1=11.5,  # Short 1st gear for aggressive hill climb & acceleration
            gear_ratio_2=6.2,   # Long 2nd gear for low-RPM highway cruising
            shift_speed_kmh=65.0
        )

        # Config 3: High-Torque Performance (Tesla Plaid / Lucid Air style)
        c3_veh = VehicleParams(
            name="Config C: Performance Dynamic",
            mass_kg=base_vehicle.mass_kg + 15.0,
            frontal_area_m2=base_vehicle.frontal_area_m2,
            drag_coefficient_cd=base_vehicle.drag_coefficient_cd,
            wheel_radius_m=base_vehicle.wheel_radius_m,
            battery_capacity_kwh=base_vehicle.battery_capacity_kwh
        )
        c3_mot = MotorParams(
            motor_type="AC Induction / Dual-PMSM",
            rated_power_kw=c1_mot.rated_power_kw * 1.45,
            peak_torque_nm=c1_mot.peak_torque_nm * 1.40,
            max_speed_rpm=18000.0
        )
        c3_trans = TransmissionParams(
            gearbox_type="Single-Speed Reduction Gearbox",
            gear_ratio_1=8.2
        )

        configs = [
            ("Config A (Single-Speed Balanced)", c1_veh, c1_mot, c1_trans),
            ("Config B (2-Speed High-Efficiency)", c2_veh, c2_mot, c2_trans),
            ("Config C (High-Performance Sport)", c3_veh, c3_mot, c3_trans),
        ]

        simulation_results = []
        for label, veh, mot, trans in configs:
            engine = EVSimulationEngine(veh, mot, trans)
            sprint = engine.simulate_acceleration_sprint(100.0, dt=0.08, max_time_s=18.0)
            t_accel = sprint["zero_to_target_time_s"] if sprint["zero_to_target_time_s"] is not None else 18.0

            # Highway 120 km/h and Urban 50 km/h consumption
            c_hwy = engine.calculate_energy_consumption(120.0)
            c_urban = engine.calculate_energy_consumption(50.0)

            # Max gradeability %
            t_wheel_max = mot.peak_torque_nm * trans.gear_ratio_1 * veh.drivetrain_efficiency
            f_tractive_max = t_wheel_max / veh.wheel_radius_m
            f_roll_crawl = veh.mass_kg * 9.81 * veh.rolling_resistance_cr
            sin_theta_max = max(0.0, min(0.65, (f_tractive_max - f_roll_crawl) / (veh.mass_kg * 9.81)))
            max_grade_pct = float(round(100.0 * (sin_theta_max / (1.0 - sin_theta_max**2)**0.5), 1))

            simulation_results.append({
                "Configuration": label,
                "Motor Type": mot.motor_type,
                "Rated Power (kW)": mot.rated_power_kw,
                "Peak Torque (Nm)": mot.peak_torque_nm,
                "Transmission": trans.gearbox_type,
                "Gear Ratio(s)": f"{trans.gear_ratio_1}:1" if trans.gearbox_type != "2-Speed Automatic" else f"G1: {trans.gear_ratio_1}:1 | G2: {trans.gear_ratio_2}:1",
                "0-100 km/h Time (s)": round(t_accel, 2),
                "Top Speed (km/h)": round(engine.vehicle_speed_from_motor_rpm(mot.max_speed_rpm, trans.gear_ratio_2 if trans.gearbox_type == "2-Speed Automatic" else trans.gear_ratio_1), 1),
                "Max Gradeability (%)": max_grade_pct,
                "Highway 120km/h (kWh/100km)": round(c_hwy["kwh_per_100km"], 2),
                "City 50km/h (kWh/100km)": round(c_urban["kwh_per_100km"], 2),
                "Est. Highway Range (km)": round(c_hwy["estimated_range_km"], 0),
                "Vehicle Mass (kg)": veh.mass_kg
            })

        # Formulate prompt for Groq LLM to analyze and explain the winner
        prompt_data = json.dumps(simulation_results, indent=2)
        system_prompt = (
            "You are a Chief EV Powertrain Architecture Specialist with deep expertise in MATLAB Powertrain Blockset, "
            "motor sizing, transmission ratios, and energy consumption physics. "
            "Write in a clear, authoritative, beautifully structured engineering format (Apple executive engineering style)."
        )

        user_prompt = f"""
Target Vehicle Requirements:
- Vehicle Mass: {base_vehicle.mass_kg} kg
- Target Top Speed: {target_top_speed_kmh} km/h
- Target Gradeability: {target_gradeability_pct} %
- Battery Pack: {base_vehicle.battery_capacity_kwh} kWh

Digital Twin Simulation Results across 3 Architectures:
{prompt_data}

Benchmark Context from Real-World EV Database:
{benchmark_evs_context}

Please provide an expert engineering evaluation:
1. **Executive Winner Recommendation**: Clearly state which configuration performs best for this vehicle profile and why.
2. **Deep-Dive Trade-off Analysis**:
   - Acceleration vs Efficiency trade-offs
   - Single-Speed vs 2-Speed Transmission trade-off (cost, gearbox mass, shift shock vs high-speed highway efficiency)
   - Gradeability & hill-start reserve
3. **Powertrain Sizing Verdict**: Recommended final motor power (kW), peak torque (Nm), and transmission reduction ratio.
4. **Actionable MATLAB/Simulink Tuning Tips**: Recommend specific parameters to refine in the next test cycle.
"""

        ai_explanation = self._call_llm(system_prompt, user_prompt, temperature=0.25)

        return {
            "configurations": simulation_results,
            "ai_verdict": ai_explanation
        }

    def chat_copilot(self, conversation_history: List[Dict], current_state_summary: str) -> str:
        """
        Interactive Powertrain Co-Pilot:
        Allows the user to ask any engineering question or request configuration adjustments.
        """
        system_prompt = f"""
You are the EV Digital Twin Powertrain Co-Pilot.
You have full access to the live digital twin simulation state:
{current_state_summary}

Guidelines:
- Give concise, highly technically accurate answers with precise numbers and units (kW, Nm, RPM, kWh/100km, %, s).
- Explain physical trade-offs (e.g. higher gear ratio increases wheel torque and hill climb ability, but reduces top speed and increases motor RPM / iron losses at cruising speeds).
- Reference real-world EV benchmarks (e.g., Porsche Taycan's 2-speed gearbox, Tesla Model 3's high-speed single reduction, Lucid Air's high-RPM miniaturized motor) when relevant.
- Keep the tone sleek, professional, and helpful (Apple-style engineering craft).
        if not self.client:
            return "[Groq API Key Required]: Please configure your GROQ_API_KEY in .env or Streamlit Cloud Secrets."

        messages = [{"role": "system", "content": system_prompt}] + conversation_history
        try:
            response = self.client.chat.completions.create(
                model=PRIMARY_MODEL,
                messages=messages,
                temperature=0.3,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception:
            try:
                response = self.client.chat.completions.create(
                    model=FALLBACK_MODEL,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=1024
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"Error interacting with AI Co-Pilot: {e}"
