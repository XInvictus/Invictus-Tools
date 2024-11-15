import os

def ascii_art():
    art = """

 ___            _  ____                _             
|_ _|_ ____   _(_)/ ___|_ __ __ _  ___| | _____ _ __ 
 | || '_ \ \ / / | |   | '__/ _` |/ __| |/ / _ \ '__|
 | || | | \ V /| | |___| | | (_| | (__|   <  __/ |   
|___|_| |_|\_/ |_|\____|_|  \__,_|\___|_|\_\___|_|   

"""
    print(art)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_passwords(path):
    return [line.strip() for line in open(path, "r", errors="ignore").readlines()]