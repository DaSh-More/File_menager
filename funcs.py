import os
from colorama import Fore


def error(text=""):
    print(f"{Fore.RED}{text}{Fore.RESET}")
    print()
    input("Для продолжения нажмите Enter...")


def colorize(text, color="red"):
    color = Fore.__getattribute__(color.upper())
    return f"{color}{text}{Fore.RESET}"


def cprint(*args, color="red", **kwargs):
    print(*map(lambda x: colorize(x, color), args), **kwargs)


def clear():
    os.system("cls")
