import utils
from texts import list_protocol, menu_text
import servers
from protocol_menu import Selecting_mode, Profil_region, manual_setting, priority_protocol_tech

#Progress is impossible without beer🍺

def menu():
    while True:
        utils.clear_terminal()
        print(menu_text)
        x = utils.digit_checker()
        if x == None:
            input("\nНажми Enter...")
            continue
        elif x == 1:
            servers.create_and_save_server()
        elif x == 2:
            print("В данном моменте не доступен")
        elif x == 3:
            servers.show_servers()         
        elif x == 4:
            utils.clear_terminal()
            servers.show_priority_servers()

        elif x == 5:
            utils.clear_terminal()
            print(list_protocol)
        elif x == 6:
            priority_protocol_tech()
        elif x == 7:
            Profil_region()
        elif x == 8:
            manual_setting()

        elif x == 9:
            Selecting_mode()
        elif x == 10:
            print("В данном моменте не доступен")
        elif x == 11:
            print("В данном моменте не доступен")
            
        elif x == 12:
            print("В данном моменте не доступен")
        elif x == 13:
            print("В данном моменте не доступен")
        
        elif x == 0:
            print("Выход...")
            break
        
        else:
            print("Неизвестная команда")
    
        input("\nНажми Enter, чтобы вернуться в меню...")


menu()