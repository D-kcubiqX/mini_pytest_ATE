import os
def clear_terminal():
    if os.name == "nt":
        os.system("cls")

    else:
        os.system("clear")

def digit_checker():
    while True:
        value = input("Введите число: ")

        if value.isdigit():
            return int(value)

        print("Нужно ввести число")
        input("Нажмите Enter...")