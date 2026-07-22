# utils.py
import os
import sys
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)

class Logger:
    @staticmethod
    def info(msg):
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}")
    
    @staticmethod
    def success(msg):
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {msg}")
    
    @staticmethod
    def warning(msg):
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {msg}")
    
    @staticmethod
    def error(msg):
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}")

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def run_command(cmd, timeout=30):
    """Run command safely"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            Logger.warning(f"Command failed: {cmd}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        Logger.error(f"Command timeout: {cmd}")
        return ""
    except Exception as e:
        Logger.error(f"Error running command: {e}")
        return ""

def check_root():
    if os.geteuid() != 0:
        Logger.error("This tool must be run as root! Use: sudo python3 main.py")
        sys.exit(1)
    Logger.success("Root privileges confirmed.")

def check_dependencies():
    tools = ["airmon-ng", "airodump-ng", "aireplay-ng", "aircrack-ng", "iw", "reaver"]
    missing = []
    
    for tool in tools:
        if not run_command(f"which {tool}"):
            missing.append(tool)
    
    if missing:
        Logger.warning(f"Missing tools: {', '.join(missing)}")
        Logger.info("Install them using: sudo apt install aircrack-ng reaver")
    else:
        Logger.success("All dependencies found!")
