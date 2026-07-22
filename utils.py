# utils.py
import os
import sys
import subprocess
import logging
from colorama import init, Fore, Style
from config import Config

# Initialize Colorama
init(autoreset=True)

class Logger:
    @staticmethod
    def setup():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("edu_wifi_audit.log"),
                logging.StreamHandler()
            ]
        )

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

def check_root():
    """Check if script is running as root."""
    if os.geteuid() != 0:
        Logger.error("Please run this tool with sudo (root privileges).")
        sys.exit(1)

def check_dependencies():
    """Check if required tools are installed."""
    missing = []
    for tool in Config.REQUIRED_TOOLS:
        if not subprocess.run(["which", tool], stdout=subprocess.PIPE).returncode == 0:
            missing.append(tool)
    
    if missing:
        Logger.error(f"Missing tools: {', '.join(missing)}")
        Logger.info("Install them using: sudo apt install aircrack-ng iw reaver pixiewps")
        sys.exit(1)
    else:
        Logger.success("All required dependencies found.")

def run_command(cmd, capture_output=True):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        if result.returncode != 0:
            Logger.warning(f"Command '{cmd}' failed: {result.stderr}")
            return None
        return result.stdout
    except Exception as e:
        Logger.error(f"Error running command: {e}")
        return None

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')