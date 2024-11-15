from colorama import Fore
from datetime import datetime

def success(message):
    print(f"{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET} • {Fore.LIGHTGREEN_EX}+{Fore.RESET} • {message}")

def error(message):
    print(f"{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET} • {Fore.LIGHTRED_EX}-{Fore.RESET} • {message}")

def info(message):
    print(f"{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET} • {Fore.LIGHTBLUE_EX}i{Fore.RESET} • {message}")

def warning(message):
    print(f"{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET} • {Fore.LIGHTYELLOW_EX}!{Fore.RESET} • {message}")

def inpt(message):
    return input(f"{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET} • {Fore.LIGHTCYAN_EX}?{Fore.RESET} • {message}")