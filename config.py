# config.py
import os

class Config:
    # Tool Name
    TOOL_NAME = "EduWiFi Auditor"
    VERSION = "1.0.0"
    
    # Required Tools Check
    REQUIRED_TOOLS = ['aircrack-ng', 'iw', 'reaver', 'pixiewps']
    
    # Default Wordlist Path (Adjust this to your Kali wordlist location)
    DEFAULT_WORDLIST = "/usr/share/wordlists/rockyou.txt"
    
    # Output Directory for Caps
    CAP_DIR = "./captured_caps"
    
    # Logging Level
    LOG_LEVEL = "INFO"