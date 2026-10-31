import os
import time
import numpy as np
import pandas as pd
from datetime import datetime

class CyberPhysicalGridObserver:
    def __init__(self, database_path="grid_quantum_ledger.csv"):
        self.db_path = database_path
        self.TRANSFORMER_BASE_HEIGHT_CM = 20.0
        self.CRITICAL_FLUID_CONDUCTIVITY = 250.0
        
        self.historical_leakage_vector = []
        self.historical_conductivity_vector = []
        
        self._boot_immutable_ledger()

    def _boot_immutable_ledger(self):
        if not os.path.exists(self.db_path):
            headers = [
                "Timestamp", "Measured_Water_Height_CM", "Inferred_Fluid_Conductivity", 
                "Calculated_Energy_Dissipation_Watts", "State_Estimation_Confidence", 
                "Grid_Isolation_Matrix", "Explosion_Risk_Index"
            ]
            pd.DataFrame(columns=headers).to_csv(self.db_path, index=False)

    def physical_environment_model(self):
        # Gradual stepping representation to simulate dynamic rainfall patterns
        true_height = round(float(np.random.uniform(5.0, 95.0)), 2)
        true_conductivity = round(float(np.random.uniform(50.0, 400.0)), 2)
        
        submerged_depth = max(0.0, true_height - self.TRANSFORMER_BASE_HEIGHT_CM)
        energy_dissipation_watts = round((submerged_depth * 0.12) * (true_conductivity * 0.08), 3)
        
        return true_height, true_conductivity, energy_dissipation_watts

    def statistical_state_observer(self, height, conductivity, energy):
        self.historical_leakage_vector.append(energy)
        self.historical_conductivity_vector.append(conductivity)
        
        if len(self.historical_leakage_vector) > 5:
            self.historical_leakage_vector.pop(0)
            self.historical_conductivity_vector.pop(0)

        variance_coefficient = np.var(self.historical_leakage_vector) if len(self.historical_leakage_vector) > 1 else 0.01
        confidence_factor = round(float(1.0 / (1.0 + (variance_coefficient * 0.001))), 4)
        risk_index = round(((height / 100.0) * 0.5) + ((conductivity / 400.0) * 0.5), 3)
        
        return confidence_factor, risk_index

    def render_dashboard(self, iteration, ts, height, conductivity, energy, confidence, risk, relay_state):
        """Clears the console screen and draws a dynamic monitoring panel."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Color coding for terminal visualizations
        if "OPEN_TRIPPED" in relay_state:
            alert_color = "🔴 [EMERGENCY TRIPPED - ISOLATED]"
        elif "STANDBY" in relay_state:
            alert_color = "🟡 [WARNING - BREACH IMMINENT]"
        else:
            alert_color = "🟢 [OPERATIONAL_NORMAL]"

        # Generating a visual load bar graph
        bar_length = int(risk * 20)
        risk_bar = "█" * bar_length + "░" * (20 - bar_length)

        print("█" * 70)
        print("          BESCOM TELEMETRY STATE ESTIMATION RADAR DASHBOARD         ")
        print("█" * 70)
        print(f" [Timestamp]: {ts}  |  [Simulation Step]: {iteration}/12")
        print("-" * 70)
        print(f"  ⚡ INSTANCE STATUS   : {alert_color}")
        print(f"  📊 EXPLOSION RISK BAR: [{risk_bar}] ({risk * 100:.1f}%)")
        print("-" * 70)
        print(f"  ▪️ Sensor Water Depth: {height:<6} cm   (Baseline Threshold: {self.TRANSFORMER_BASE_HEIGHT_CM} cm)")
        print(f"  ▪️ Fluid Ion Cond.   : {conductivity:<6} mS/m (Critical Cutoff  : {self.CRITICAL_FLUID_CONDUCTIVITY} mS/m)")
        print(f"  ▪️ Energy Dissipation: {energy:<6} Watts")
        print(f"  ▪️ Matrix Confidence : {confidence * 100:<6} %")
        print("-" * 70)
        print(f"  💾 Localized Ledger DB Sync: [ACTIVE] -> Written to: {self.db_path}")
        print("█" * 70)

    def execute_deterministic_relay(self, iteration, height, conductivity, energy, confidence, risk):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        relay_state = "CLOSED (GRID_LIVE)"
        
        if risk > 0.72 or (height > 60.0 and conductivity > self.CRITICAL_FLUID_CONDUCTIVITY):
            relay_state = "OPEN_TRIPPED (SYSTEM_ISOLATED)"
        elif height > self.TRANSFORMER_BASE_HEIGHT_CM:
            relay_state = "STANDBY_WARNING"

        # Display the terminal control desk dashboard
        self.render_dashboard(iteration, timestamp, height, conductivity, energy, confidence, risk, relay_state)

        # Log to ledger frame
        log_packet = pd.DataFrame([{
            "Timestamp": timestamp,
            "Measured_Water_Height_CM": height,
            "Inferred_Fluid_Conductivity": conductivity,
            "Calculated_Energy_Dissipation_Watts": energy,
            "State_Estimation_Confidence": confidence,
            "Grid_Isolation_Matrix": relay_state,
            "Explosion_Risk_Index": risk
        }])
        log_packet.to_csv(self.db_path, mode='a', header=False, index=False)

    def run_observer_loop(self, cycles=12):
        for iteration in range(1, cycles + 1):
            h, c, e = self.physical_environment_model()
            conf, risk = self.statistical_state_observer(h, c, e)
            self.execute_deterministic_relay(iteration, h, c, e, conf, risk)
            time.sleep(1.5) # Refresh rate

if __name__ == "__main__":
    engine = CyberPhysicalGridObserver()
    engine.run_observer_loop()
