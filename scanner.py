# scanner.py
import subprocess
import time
import re
from utils import run_command, Logger

class WifiScanner:
    def __init__(self):
        self.interface = None
        self.monitor_interface = None

    def get_interfaces(self):
        """List wireless interfaces"""
        output = run_command("iw dev | grep Interface")
        interfaces = [line.split()[-1] for line in output.splitlines() if line.strip()]
        return interfaces

    def enable_monitor_mode(self, interface):
        """Enable monitor mode properly"""
        Logger.info(f"Enabling monitor mode on {interface}...")
        
        # Kill interfering processes
        run_command("airmon-ng check kill")
        
        # Start monitor mode
        result = run_command(f"airmon-ng start {interface}")
        
        # Get monitor interface name (usually wlan0mon or wlan1mon)
        mon_output = run_command("iw dev | grep -E 'Interface.*mon'")
        if "mon" in mon_output:
            self.monitor_interface = mon_output.split()[-1]
            Logger.success(f"Monitor mode enabled: {self.monitor_interface}")
            return self.monitor_interface
        else:
            # Fallback
            self.monitor_interface = f"{interface}mon"
            Logger.warning("Could not detect monitor interface, using fallback.")
            return self.monitor_interface

    def scan_networks(self, interface, duration=15):
        """Improved network scanning"""
        if not self.monitor_interface:
            self.enable_monitor_mode(interface)
        
        mon_iface = self.monitor_interface or interface
        
        Logger.info(f"Scanning networks on {mon_iface} for {duration} seconds...")
        
        # Run airodump-ng and save to file for reliable parsing
        cap_file = f"/tmp/scan_{int(time.time())}.csv"
        
        cmd = f"timeout {duration} airodump-ng {mon_iface} -w /tmp/scan --output-format csv"
        run_command(cmd)
        
        # Parse the CSV
        networks = self._parse_airodump_csv("/tmp/scan-01.csv")
        
        if not networks:
            Logger.warning("No networks found. Trying alternative scan...")
            networks = self._fallback_scan(mon_iface)
        
        return networks

    def _parse_airodump_csv(self, csv_path):
        """Parse airodump-ng CSV output"""
        networks = []
        try:
            with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for line in lines[2:]:  # Skip headers
                if line.strip() and "," in line:
                    parts = line.strip().split(',')
                    if len(parts) > 5 and parts[0].strip() and parts[13].strip() != " ":
                        try:
                            bssid = parts[0].strip()
                            ssid = parts[13].strip() if parts[13].strip() else "Hidden"
                            channel = parts[3].strip()
                            signal = parts[8].strip()
                            encryption = parts[5].strip() + " " + parts[6].strip()
                            
                            if bssid and len(bssid) > 10:
                                networks.append({
                                    "BSSID": bssid,
                                    "SSID": ssid[:20],
                                    "Channel": channel,
                                    "Signal": signal,
                                    "Encryption": encryption[:15]
                                })
                        except:
                            continue
        except:
            pass
        
        return networks[:15]  # Limit to 15 networks

    def _fallback_scan(self, interface):
        """Fallback if CSV fails"""
        Logger.info("Using fallback iw scan...")
        output = run_command(f"iw dev {interface} scan | head -n 100")
        # Simple parsing (basic)
        networks = []
        # ... (can improve later)
        return networks
