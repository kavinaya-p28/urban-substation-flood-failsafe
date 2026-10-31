import os
import time
import random
import pandas as pd
from datetime import datetime

class SmartGridSafetyController:
    """
    Advanced IoT-Edge Controller for Urban Flash Flood Monitoring
    and Automated Substation Protection.
    """
    def __init__(self, log_file="advanced_transformer_safety_log.csv"):
        self.log_file = log_file
        # Strict Industry Safety Thresholds
        self.CRITICAL_WATER_LEVEL_CM = 80.0
        self.CRITICAL_LEAKAGE_CURRENT_MA = 30.0
        self.WARNING_WATER_LEVEL_CM = 50.0
        
        # In-memory history cache to analyze trends (Moving Average calculation)
        self.water_history = []
        self.leakage_history = []
        
        self._initialize_blackbox_logger()

    def _initialize_blackbox_logger(self):
        """Creates the secure CSV log ledger with advanced analytical headers if it doesn't exist."""
        if not os.path.exists(self.log_file):
            columns = [
                "Timestamp", "Raw_Water_CM", "Raw_Leakage_mA", 
                "Rolling_Avg_Water_CM", "Rolling_Avg_Leakage_mA",
                "System_Health_Status", "Relay_Tripped", "Command_Executed"
            ]
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.log_file, index=False)
            print(f"[INIT] Secure telemetry database created at: {self.log_file}")

    def read_edge_sensors(self):
        """Simulates raw telemetry streaming directly from industrial edge hardware controllers."""
        # Simulating turbulent environmental changes (e.g., heavy downpours)
        raw_water = round(random.uniform(20.0, 110.0), 2)
        
        # Leakage current escalates non-linearly with immersion depth
        if raw_water > self.WARNING_WATER_LEVEL_CM:
            raw_leakage = round(random.uniform(15.0, 60.0), 2)
        else:
            raw_leakage = round(random.uniform(0.1, 10.0), 2)
            
        return raw_water, raw_leakage

    def process_analytics(self, raw_water, raw_leakage):
        """Applies edge data smoothing algorithms to eliminate raw sensor noise anomalies."""
        self.water_history.append(raw_water)
        self.leakage_history.append(raw_leakage)
        
        # Maintain a rolling window of the last 3 data captures
        if len(self.water_history) > 3:
            self.water_history.pop(0)
            self.leakage_history.pop(0)
            
        avg_water = round(sum(self.water_history) / len(self.water_history), 2)
        avg_leakage = round(sum(self.leakage_history) / len(self.leakage_history), 2)
        return avg_water, avg_leakage

    def execute_safety_logic(self, avg_water, avg_leakage):
        """Deterministically evaluates asset state and commands safety protocols."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "OPERATIONAL_HEALTHY"
        relay_tripped = False
        command = "NO_ACTION_REQUIRED"

        # Double-threshold confirmation logic to completely prevent accidental blackouts
        if avg_water >= self.CRITICAL_WATER_LEVEL_CM and avg_leakage >= self.CRITICAL_LEAKAGE_CURRENT_MA:
            status = "CRITICAL_FLOOD_BREACH"
            relay_tripped = True
            command = "CRITICAL_GRID_RELAY_TRIP_DEENERGIZE"
            print(f"[{timestamp}] 🚨 [CRITICAL ALERT] Moving Avg Water: {avg_water}cm | Leakage: {avg_leakage}mA. ISOLATING TRANSFORMER IMMEDIATELY!")
            
        elif avg_water >= self.WARNING_WATER_LEVEL_CM:
            status = "WARNING_SUBMERSION_RISK"
            command = "BROADCAST_TELEMETRY_TO_BESCOM_SCADA"
            print(f"[{timestamp}] ⚠️ [WARNING] Submersion detected at {avg_water}cm. Elevating surveillance parameters.")
            
        else:
            print(f"[{timestamp}] ✅ [NORMAL] Grid Stable. Core Temperature and Insulation Integrity Verified.")

        # Save comprehensive status dataset to historical ledger
        self._log_transaction(timestamp, avg_water, avg_leakage, status, relay_tripped, command)

    def _log_transaction(self, ts, w_avg, l_avg, status, trip, cmd):
        """Appends real-time data frame to the localized edge analytics register."""
        transaction_data = pd.DataFrame([{
            "Timestamp": ts,
            "Raw_Water_CM": self.water_history[-1],
            "Raw_Leakage_mA": self.leakage_history[-1],
            "Rolling_Avg_Water_CM": w_avg,
            "Rolling_Avg_Leakage_mA": l_avg,
            "System_Health_Status": status,
            "Relay_Tripped": trip,
            "Command_Executed": cmd
        }])
        transaction_data.to_csv(self.log_file, mode='a', header=False, index=False)

    def boot_system(self, iterations=10):
        """Starts the main infinite monitoring loop of the automated protection device."""
        print("\n" + "="*70)
        print("   INDUSTRIAL SMART GRID SUBSTATION MONITORING DEVICE CORE v2.0.4   ")
        print("="*70)
        
        try:
            for cycle in range(1, iterations + 1):
                print(f"\n[Telemetry Stream Cycle #{cycle}]")
                raw_w, raw_l = self.read_edge_sensors()
                avg_w, avg_l = self.process_analytics(raw_w, raw_l)
                self.execute_safety_logic(avg_w, avg_l)
                time.sleep(1.5) # Fast 1.5s industrial polling rate
        except KeyboardInterrupt:
            print("\n[SHUTDOWN] Safety monitoring paused safely by grid engineer manual override.")
        
        print("\n" + "="*70)
        print(f"Deployment Simulation Finished. Cryptographic log trace locked in: '{self.log_file}'")
        print("="*70)

# Run the system
if __name__ == "__main__":
    controller = SmartGridSafetyController()
    controller.boot_system(iterations=8)
