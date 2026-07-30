import os
def clear_terminal():
    if os.name == "nt":
        os.system("cls")

    else:
        os.system("clear")

def digit_checker(value):
    if not value.isdigit():
        print("Нужно ввести число")
        return None

    return int(value)