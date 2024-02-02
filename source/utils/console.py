import os
import pyfiglet
import shutil
import ctypes
from getpass import getpass
from datetime import datetime
from colorama import Fore, Style
from source.utils.configloader import *

def setTitle(title: str):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def logo():
    columns, rows = shutil.get_terminal_size()
    ascii_text = pyfiglet.figlet_format("VisionaryX", font="fender")
    lines = ascii_text.split("\n")
    positions = []
    x = int(columns / 2 - len(max(lines, key=len)) / 2)
    for i in range(len(lines)):
        y = int(rows / 2 - len(lines) / 2 + i)
        positions.append(y)

    print("\033[1m\033[36m", end="")
    for i in range(len(lines)):
        print(f"\033[{positions[i]};{x}H{lines[i]}")

    print("\033[1m\033[33;7m", end="")
    versionText = f"Version: {visionaryXVersion}"
    versionText_x = int(columns / 2 - len(versionText) / 2)
    versionText_y = positions[-1] + 2
    print(f"\033[{versionText_y};{versionText_x}H{versionText}")

    createdText = "Created by visions4k"
    createdText_x = int(columns / 2 - len(createdText) / 2)
    createdText_y = versionText_y + 1 
    print(f"\033[{createdText_y};{createdText_x}H{createdText}")

    print("\033[0m", end="")
    print("\n")
    
def clear():
    if 'nt' in os.name:
        os.system('cls')
    else:
        os.system('clear')

def timet():
       return Style.BRIGHT + Fore.BLACK + f"[{datetime.now().strftime('%I:%M:%S')}] "

def log(object):
    print(
        f"{timet()}{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}INFO {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{object}",
        end="\n",
    )

def ok(object):
    print(
        f"{timet()}{Style.BRIGHT}{Fore.LIGHTGREEN_EX}BUILD {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{object}",
        end="\n",
    )
    
def okreq(object):
    print(
        f"{timet()}{Style.BRIGHT}{Fore.LIGHTGREEN_EX}200 {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{object}",
        end="\n",
    )
    
def fatalreq(object, code):
    print(
        f"{timet()}{Style.BRIGHT}{Fore.LIGHTRED_EX}{code} {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{object}",
        end="\n",
    )

def important(object):
    print(
        f"{timet()}{Style.BRIGHT}{Fore.LIGHTRED_EX}IMPORTANT {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{object}",
        end="\n",
    )
    
def fatal(object):
    print(
        f"{timet()}{Style.BRIGHT}{Fore.LIGHTRED_EX}ERROR {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{object}",
        end="\n",
    )
    
def warn(object):
    print(
        f"{timet()}{Style.BRIGHT}{Fore.LIGHTRED_EX}WARN {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{object}",
        end="\n",
    )

def option(object):
    print(
        f"{timet()}{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX}PICK {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{object}",
        end="\n",
    )

def found(object):
    print(
        f"{timet()}{Style.BRIGHT}{Fore.LIGHTCYAN_EX}SCRAPER {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{object}",
        end="\n",
    )
    
def counter(object):
    print(
        f"{timet()}{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}GROUPS CLAIMED {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{object}",
        end="\r",
    )

def inputt(prompt):
    return input(
        f"{timet()}{Style.BRIGHT}{Fore.LIGHTBLUE_EX}ENTER HERE {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{prompt}"
    )

def sinputt(prompt):
    return getpass(
        f"{timet()}{Style.BRIGHT}{Fore.LIGHTBLUE_EX}ENTER HERE {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{prompt}"
    )
    
    
