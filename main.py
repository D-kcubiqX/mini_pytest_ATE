import utils
from texts import menu_text, list_protocol
import servers
from protocol_menu import block_protocol_menu, Selecting_mode
import scores

#Progress is impossible without beer🍺

def menu():
    while True:
        global final_score
        global base_scores 
        global region_score 
        global mode_scores
        utils.clear_terminal()
        print(menu_text)
        choice = input("Введите в этом поле: ")

        if not choice.isdigit():
            print("Нужно ввести число")
            input("\nНажми Enter...")
            continue

        x = int(choice)

        if x == 1:
            servers.generate_server_stats()
        elif x == 2:
            block_protocol_menu()
        elif x == 3:
            pass
        elif x == 4:
            utils.clear_terminal()
            print(list_protocol)
        elif x == 5:
            utils.clear_terminal()
            print("по умолчанию")
            for protocol, score in scores.base_scores.items():
                print(f"{protocol:15} : {score:+4}")
            print("----------------------------------")
            print("Региональная оценка")
            for protocol, score in scores.region_score.items():
                print(f"{protocol:15} : {score:+4}")
            print("----------------------------------")
            print("Режим")
            for protocol, score in scores.mode_scores.items():
                print(f"{protocol:15} : {score:+4}")
            print("----------------------------------")
            print("Итог (сумма по умолчанию, заблокированых протоколов, режим и по сортировки лучший --> худший)")
            scores.calcul_result()
            sorted_final = sorted(
                scores.final_score.items(),
                key=lambda x: x[1],
                reverse=True
            )
            for protocol, score in sorted_final:
                print(f"{protocol:15} : {score:+4}")

        elif x == 6:
            Selecting_mode()
        elif x == 7:
            pass

        elif x == 0:
            print("Выход...")
            break

        else:
            print("Неизвестная команда")

        input("\nНажми Enter, чтобы вернуться в меню...")


menu()