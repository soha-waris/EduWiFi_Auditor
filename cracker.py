# cracker.py
import subprocess
from utils import run_command, Logger
import os

class WifiCracker:
    def __init__(self):
        pass

    def crack_handshake(self, cap_prefix, wordlist="/usr/share/wordlists/rockyou.txt"):
        """Run aircrack-ng on the captured .cap file."""
        
        # Ensure path ends with .cap for aircrack
        if not cap_prefix.endswith('.cap'):
            cap_file = f"{cap_prefix}.cap"
        else:
            cap_file = cap_prefix

        if not os.path.exists(cap_file):
            Logger.error(f"Cap file not found: {cap_file}")
            return

        Logger.info(f"Cracking {cap_file} using {wordlist}...")
        
        cmd = f"aircrack-ng -w {wordlist} {cap_file}"
        output = run_command(cmd)
        
        if output:
            # Parse aircrack output for the key
            lines = output.split('\n')
            for line in lines:
                if "KEY FOUND!" in line or "Key" in line:
                    Logger.success(line.strip())
                    return True
        
        Logger.warning("Password not found in wordlist.")
        return False