"""
EV Master Dataset & Benchmarking Engine
Loads and indexes the 175+ real EV vehicles in EV_master_dataset_all_vehicles.csv.
Provides fast nearest-neighbor matching, segment statistics, and baseline calibration.
"""

import os
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from typing import Dict, List, Optional, Tuple

DATASET_FILENAME = "EV_master_dataset_all_vehicles.csv"

class EVDatasetManager:
    def __init__(self, csv_path: Optional[str] = None):
        if csv_path is None:
            csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATASET_FILENAME)
        
        self.csv_path = csv_path
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"EV Master Dataset not found at: {self.csv_path}")

        self.df = pd.read_csv(self.csv_path)
        # Clean numerical columns
        num_cols = ['Mass (kg)', 'Top Speed (km/h)', 'Peak Torque (Nm)', 'Target Gradeability (%)']
        for col in num_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0.0)

        self.features = num_cols
        # Normalized feature matrix for KNN
        self.df_normalized = self.df[self.features].copy()
        self.means = self.df_normalized.mean()
        self.stds = self.df_normalized.std() + 1e-6
        self.scaled_features = (self.df_normalized - self.means) / self.stds

        self.knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
        self.knn.fit(self.scaled_features)

    def get_vehicle_list(self) -> List[str]:
        """Returns sorted list of vehicle names from dataset."""
        return sorted(self.df['Vehicle Model'].dropna().unique().tolist())

    def get_vehicle_specs(self, model_name: str) -> Optional[Dict]:
        """Retrieves exact specs of a named vehicle model."""
        match = self.df[self.df['Vehicle Model'] == model_name]
        if match.empty:
            return None
        row = match.iloc[0]
        return {
            "name": row['Vehicle Model'],
            "segment": row['Segment'],
            "mass_kg": float(row['Mass (kg)']),
            "top_speed_kmh": float(row['Top Speed (km/h)']),
            "peak_torque_nm": float(row['Peak Torque (Nm)']),
            "target_gradeability_pct": float(row['Target Gradeability (%)']),
            "powertrain_type": str(row['Powertrain Type']),
            "transmission": str(row['Gearbox / Transmission'])
        }

    def find_similar_evs(self, mass_kg: float, top_speed_kmh: float, peak_torque_nm: float, gradeability_pct: float, k: int = 4) -> pd.DataFrame:
        """Finds top-k closest production EVs using normalized Euclidean distance."""
        query = pd.DataFrame([{
            'Mass (kg)': mass_kg,
            'Top Speed (km/h)': top_speed_kmh,
            'Peak Torque (Nm)': peak_torque_nm,
            'Target Gradeability (%)': gradeability_pct
        }])
        query_scaled = (query - self.means) / self.stds
        distances, indices = self.knn.kneighbors(query_scaled, n_neighbors=min(k, len(self.df)))

        matches = self.df.iloc[indices[0]].copy()
        matches['Similarity (%)'] = np.round(100.0 / (1.0 + distances[0]), 1)
        return matches[['Vehicle Model', 'Segment', 'Mass (kg)', 'Top Speed (km/h)', 'Peak Torque (Nm)', 'Target Gradeability (%)', 'Powertrain Type', 'Gearbox / Transmission', 'Similarity (%)']]

    def get_segment_averages(self, segment: str) -> Dict:
        """Returns mean statistics for a vehicle segment."""
        sub = self.df[self.df['Segment'] == segment]
        if sub.empty:
            return {}
        return {
            "count": len(sub),
            "avg_mass": float(sub['Mass (kg)'].mean()),
            "avg_top_speed": float(sub['Top Speed (km/h)'].mean()),
            "avg_torque": float(sub['Peak Torque (Nm)'].mean()),
            "avg_gradeability": float(sub['Target Gradeability (%)'].mean())
        }
