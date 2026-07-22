# main.py
import sys
import os
from utils import clear_screen, Logger, check_root, check_dependencies
from scanner import WifiScanner
from attacker import WifiAttacker
from cracker import WifiCracker
from wps_attack import WPSAttacker
from config import Config

class EduWiFiAuditor:
    def __init__(self):
        clear_screen()
        self.disclaimer()
        check_root()
        check_dependencies()
        
        Logger.info(f"Initializing {Config.TOOL_NAME} v{Config.VERSION}")
        
        # Initialize Components
        self.scanner = WifiScanner()
        self.attacker = None # Initialized after interface selection
        self.cracker = WifiCracker()
        self.wps = None

    def disclaimer(self):
        print(f"""
{Fore.CYAN}===============================================
   {Config.TOOL_NAME} - Educational Use Only
===============================================
   Author: HackerGPT (White Hack Labs)
   Purpose: Authorized Penetration Testing
        
   Disclaimer:
   This tool is for educational purposes only.
   Do not use on networks you do not own or 
   have explicit permission to test.
{Style.RESET_ALL}""")

    def select_interface(self):
        """Allow user to select WiFi interface."""
        Logger.info("Scanning for wireless interfaces...")
        ifaces = self.scanner.get_interfaces()
        
        if not ifaces:
            Logger.error("No wireless interfaces found. Check your adapter.")
            sys.exit(1)

        print(f"\n{Fore.YELLOW}Select Interface:{Style.RESET_ALL}")
        for i, iface in enumerate(ifaces):
            print(f"  {i+1}. {iface}")
        
        try:
            choice = int(input("\nEnter number: ")) - 1
            if 0 <= choice < len(ifaces):
                selected = ifaces[choice]
                Logger.info(f"Selected Interface: {selected}")
                
                # Setup Attacker and WPS with this interface
                self.attacker = WifiAttacker(selected)
                self.wps = WPSAttacker(selected)
                
                return selected
            else:
                Logger.error("Invalid choice.")
                return None
        except ValueError:
            Logger.error("Please enter a number.")
            return None

    def scan_menu(self, interface):
        """Menu for scanning and selecting target."""
        while True:
            clear_screen()
            print(f"{Fore.CYAN}--- Network Scanner ({interface}) ---{Style.RESET_ALL}")
            
            networks = self.scanner.scan_networks(interface)
            
            if not networks:
                Logger.warning("No networks found.")
                break

            # Display Table (Simple format)
            print(f"{'#':<4} {'SSID':<20} {'BSSID':<18} {'CH':<5} {'Signal':<10} {'Enc'}")
            print("-" * 70)
            for idx, net in enumerate(networks):
                print(f"{idx+1:<4} {net['SSID']:<20} {net['BSSID']:<18} {net['Channel']:<5} {net['Signal']:<10} {net['Encryption']}")
            
            print("\nOptions:")
            print("  1. Select Target")
            print("  2. Rescan")
            print("  3. Main Menu")
            print("  4. Exit")
            
            choice = input("\nEnter choice: ")
            
            if choice == '1':
                try:
                    idx = int(input("Select Target Number: ")) - 1
                    if 0 <= idx < len(networks):
                        target = networks[idx]
                        Logger.info(f"Selected Target: {target['SSID']}")
                        self.target_menu(target, interface)
                    else:
                        Logger.error("Invalid target.")
                except ValueError:
                    pass
            elif choice == '2':
                continue
            elif choice == '3':
                break
            elif choice == '4':
                sys.exit(0)

    def target_menu(self, target, interface):
        """Menu for attacking the selected target."""
        while True:
            clear_screen()
            print(f"{Fore.YELLOW}--- Target: {target['SSID']} ({target['BSSID']}) ---{Style.RESET_ALL}")
            print(f"Channel: {target['Channel']} | Encryption: {target['Encryption']}")
            
            print("\nOptions:")
            print("  1. Deauth Attack")
            print("  2. Capture Handshake")
            print("  3. Crack Handshake")
            print("  4. WPS Attack (Reaver)")
            print("  5. Back to Scan")
            print("  6. Exit Tool")
            
            choice = input("\nEnter choice: ")
            
            if choice == '1':
                count = input("Number of deauth packets (default 100): ") or "100"
                self.attacker.deauth_attack(target['BSSID'], count=count)
                
            elif choice == '2':
                cap_path = self.attacker.capture_handshake(
                    target['BSSID'], 
                    target['Channel'], 
                    target['SSID']
                )
                if cap_path:
                    input("Press Enter to continue...")
                    
            elif choice == '3':
                # Find the most recent cap file for this SSID
                cap_prefix = f"./captured_caps/{target['SSID']}_cap"
                self.cracker.crack_handshake(cap_prefix)
                input("Press Enter to continue...")

            elif choice == '4':
                if target['Encryption'] == 'WPS' or input("Is this network WPS enabled? (y/n): ").lower() == 'y':
                    self.wps.attack_reaver(target['BSSID'], target['Channel'])
                else:
                    Logger.warning("WPS Attack requires WPS enabled.")

            elif choice == '5':
                break
            elif choice == '6':
                sys.exit(0)

    def run(self):
        """Main execution loop."""
        while True:
            clear_screen()
            print(f"{Fore.CYAN}--- {Config.TOOL_NAME} Main Menu ---{Style.RESET_ALL}")
            print("  1. Start Auditing")
            print("  2. Exit")
            
            choice = input("\nEnter choice: ")
            if choice == '1':
                interface = self.select_interface()
                if interface:
                    self.scan_menu(interface)
            elif choice == '2':
                Logger.info("Exiting EduWiFi Auditor...")
                sys.exit(0)

if __name__ == "__main__":
    app = EduWiFiAuditor()
    app.run()