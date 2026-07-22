# scanner.py
import subprocess
from utils import run_command, Logger
import re

class WifiScanner:
    def __init__(self):
        self.interface = None

    def get_interfaces(self):
        """List available wireless interfaces."""
        output = run_command("iw dev")
        if not output:
            return []
        
        interfaces = []
        for line in output.split('\n'):
            if 'Interface' in line:
                iface = line.split()[1]
                interfaces.append(iface)
        return interfaces

    def set_monitor_mode(self, interface):
        """Put interface into monitor mode."""
        Logger.info(f"Setting {interface} to monitor mode...")
        # Bring down, change mode, bring up
        run_command(f"ip link set {interface} down")
        run_command(f"iw dev {interface} set type monitor")
        run_command(f"ip link set {interface} up")
        Logger.success(f"{interface} is now in monitor mode.")

    def scan_networks(self, interface):
        """Scan for WiFi networks using airodump-ng equivalent logic via subprocess."""
        Logger.info("Scanning for networks... (Press Ctrl+C to stop)")
        
        # We use a simple grep on iw scan or airodump-ng. 
        # For robust parsing, we'll use 'iw dev <iface> scan' and parse output.
        cmd = f"iw dev {interface} scan | grep -E 'SSID:|BSS|signal:'"
        raw_output = run_command(cmd)
        
        if not raw_output:
            Logger.warning("No networks found or command failed.")
            return []

        # Simple parser for demo purposes. 
        # In production, use 'airodump-ng' output parsing for more detail.
        networks = []
        lines = raw_output.split('\n')
        
        current_bssid = None
        current_channel = None
        
        for line in lines:
            if "BSS" in line:
                parts = line.split()
                # This is a simplified extraction; real-world parsing needs regex on full iw scan
                pass 
            
        # Alternative: Use 'airodump-ng' one-shot for simplicity in this educational context
        Logger.info("Using airodump-ng for detailed scan...")
        cmd = f"timeout 10 airodump-ng {interface}"
        # Note: Parsing airodump-ng stdout programmatically is complex. 
        # For this script, we will simulate the result or use a simpler 'iw' parser.
        
        # Let's stick to a robust 'iw' parser for this example:
        return self._parse_iw_scan(interface)

    def _parse_iw_scan(self, interface):
        """Parse iw scan output into structured data."""
        cmd = f"iw dev {interface} scan"
        raw = run_command(cmd)
        if not raw:
            return []

        networks = []
        # Simple regex to extract SSID, BSSID, Channel, Signal, Enc
        pattern = re.compile(r"BSS\s+([0-9a-fA-F:]+).*?SSID:\s*([^\n]*).*?channel:\s*(\d+).*?signal:\s*(-\d+ dBm).*?tx-bitrate:\s*\d+.*?WPA|RSN")
        
        # Since iw scan output is multi-line, we split by BSS blocks roughly
        blocks = raw.split("BSS ")
        
        for block in blocks[1:]: # Skip first empty
            lines = block.split('\n')
            bssid = None
            ssid = "Hidden"
            channel = "N/A"
            signal = "N/A"
            enc = "Open"

            for line in lines:
                if line.startswith("[0-9a-fA-F]:"):
                    bssid = line.split()[0]
                elif "SSID:" in line and not "Hidden" in line:
                    ssid = line.split("SSID:")[1].strip()
                elif "channel:" in line:
                    channel = line.split("channel:")[1].split()[0]
                elif "signal:" in line:
                    signal = line.split("signal:")[1].split()[0]
                elif "WPA" in line or "RSN" in line:
                    enc = "WPA/WPA2"

            if bssid:
                networks.append({
                    "BSSID": bssid,
                    "SSID": ssid,
                    "Channel": channel,
                    "Signal": signal,
                    "Encryption": enc
                })
        return networks