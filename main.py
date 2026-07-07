import random
import utils
from texts import menu_text, menu_block, list_protocol, Selecting_mode_menu, menu_block_protocol, menu_block_profile
import servers

protocols = [
    "OpenVPN", 
    "WireGuard", 
    "AmneziaWG", 
    "Lightway", 
    "SoftEther", 
    "IKEv2/IPSec", 
    "SSTP", 
    "SOCKS5", 
    "HTTP Proxy", 
    "Shadowsocks", 
    "Trojan", 
    "VLESS", 
    "VMess", 
    "Hysteria", 
    "Hysteria2",
    "QUIC",
    "TUIC", 
    "NaiveProxy", 
    "SSH Tunnel", 
    "MTProto Proxy"
    ]

scores = {}
base_scores = {}
blocked_scores = {}
mode_scores = {}
current_mode = 0
final_score = {}

for protocol in protocols:
    scores[protocol] = 0
    base_scores[protocol] = 0
    blocked_scores[protocol] = 0
    mode_scores[protocol] = 0
    final_score[protocol] = 0

#для оценки:
#100  = рекомендую
#50   = скорее хорошо
#0    = неизвестно/нейтрально
#-50  = скорее плохо
#-100 = плохо
#-200 = почти исключить

# для оценки
#0   — практически не определяется
#20  — определяется редко
#40  — определяется
#60  — определяется хорошо
#80  — определяется очень хорошо
#100 — сигнатура известна


MIN_SCORE = -200
MAX_SCORE = 200

def clamp_score(value):
    return max(MIN_SCORE, min(MAX_SCORE, value))

def block_protocol_menu():
    #Регион / Провайдер
    #DPI
    #UDP Block
    #QUIC Block
    #WireGuard Detection
    #OpenVPN Detection
    #VLESS Detection
    global blocked_scores
    utils.clear_terminal()
    print(menu_block)
    mb_choice = input("Введите в этом поле: ")
    if not mb_choice.isdigit():
        print("Нужно ввести число")
        return
    mb_choice1 = int(mb_choice)
    if mb_choice1 == 0:
        return
    if mb_choice1 == 1:
        #Надо ещё разблокировку сделать
        global blocked_scores
        utils.clear_terminal()
        print(menu_block_protocol)
        choice = input("Введите в этом поле: ")
        if not choice.isdigit():
            print("Нужно ввести число")
            return
        protocol_block = int(choice)
        if protocol_block == 0:
            return
        if 1 <= protocol_block <= len(protocols):
            blocked_protocol = protocols[protocol_block - 1]
            print("Регион блокирует:", blocked_protocol)
            blocked_scores[blocked_protocol] = -200
            calcul_result()
            print("Очки протокола теперь:", blocked_scores[blocked_protocol])
        else:
            print("Такого протокола нет")
    if mb_choice1 == 2:
        utils.clear_terminal()
        print(menu_block_profile)
        choice = input("Введите в этом поле: ")
        if not choice.isdigit():
            print("Нужно ввести число")
            return
        profile_block = int(choice)
        if profile_block == 0:
            return
        if profile_block == 1:
            blocked_scores.update({
                "OpenVPN": -200, #Обнаруживаются легко
                "WireGuard": -200, #Обнаруживаются легко
                "AmneziaWG": 100, #Наиболее устойчивые к DPI
                "Lightway": 100, #Наиболее устойчивые к DPI. Но айпи адрес сервеса блокируется
                "SoftEther": -200, #Обнаруживаются легко
                "IKEv2/IPSec": -200, #Обнаруживаются легко
                "SSTP": -200, #Обнаруживаются легко
                "SOCKS5": -200, #Обнаруживаются легко
                "HTTP Proxy": -200, #Обнаруживаются легко
                "Shadowsocks": -100, #Обнаруживаются
                "Trojan": -100, #Обнаруживаются
                "VLESS": -100, #чистый обнаруживаются
                "VMess": -100, #чистый обнаруживаются
                "Hysteria": 100, #Наиболее устойчивые к DPI
                "Hysteria2": 100, #Наиболее устойчивые к DPI
                "QUIC": 0, # хз
                "TUIC": 100, #Наиболее устойчивые к DPI
                "NaiveProxy": 100, #Наиболее устойчивые к DPI
                "SSH Tunnel": -100, #Обнаруживаются
                "MTProto Proxy": -100 #Обнаруживаются
            })
            calcul_result()
            print("Применён профиль")

        if profile_block == 2:
            blocked_scores.update({
                "OpenVPN": -200, #Обнаруживаются легко
                "WireGuard": -200, #Обнаруживаются легко
                "AmneziaWG": 50, #Работают при правильной настройке
                "Lightway": 0, #нет информации
                "SoftEther": 0, #нет информации
                "IKEv2/IPSec": -200, #Обнаруживаются легко
                "SSTP": -200, #Обнаруживаются легко
                "SOCKS5": -200, #Обнаруживаются легко
                "HTTP Proxy": -200, #Обнаруживаются легко
                "Shadowsocks": -100, #Обнаруживаются
                "Trojan": -100, #Обнаруживаются
                "VLESS": -100, #чистый обнаруживаются
                "VMess": -100, #чистый обнаруживаются
                "Hysteria": 0, # нет информации
                "Hysteria2": 50, #Работают при правильной настройке
                "QUIC": 0, # нет информации
                "TUIC": 50, #Работают при правильной настройке
                "NaiveProxy": 50, #Работают при правильной настройке
                "SSH Tunnel": -100, #Обнаруживаются
                "MTProto Proxy": 0 #нет информации
            })
            calcul_result()
            print("Применён профиль")
            
        if profile_block == 3:
            blocked_scores.update({
                "OpenVPN": -200, #Обнаруживаются легко
                "WireGuard": -200, #Обнаруживаются легко
                "AmneziaWG": -150, #Обнаруживаются через час или день
                "Lightway": 0, #нет информации
                "SoftEther": 0, #нет информации
                "IKEv2/IPSec": -200, #Обнаруживаются легко
                "SSTP": -200, #Обнаруживаются легко
                "SOCKS5": -200, #Обнаруживаются легко
                "HTTP Proxy": -200, #Обнаруживаются легко
                "Shadowsocks": -200, #Обнаруживаются легко
                "Trojan": 0, #нет информации
                "VLESS": 0, #про чистый нет информации
                "VMess": 0, #про чистый нет информации
                "Hysteria": 0, # нет информации
                "Hysteria2": -150, #Обнаруживаются через час или день
                "QUIC": -150, #Обнаруживаются через час или день
                "TUIC": -150, #Обнаруживаются через час или день
                "NaiveProxy": 0, #нет информации
                "SSH Tunnel": -200, #Обнаруживаются легко
                "MTProto Proxy": 0 #нет информации
            })
            calcul_result()
            print("Применён профиль")

        if profile_block == 4:
            blocked_scores.update({
                "OpenVPN": -200, #Обнаруживаются легко
                "WireGuard": -200, #Обнаруживаются легко
                "AmneziaWG": -150, #Обнаруживаются через час или день
                "Lightway": 0, #нет информации
                "SoftEther": 0, #нет информации
                "IKEv2/IPSec": -200, #Обнаруживаются легко
                "SSTP": -200, #Обнаруживаются легко
                "SOCKS5": -200, #Обнаруживаются легко
                "HTTP Proxy": -200, #Обнаруживаются легко
                "Shadowsocks": -200, #Обнаруживаются легко
                "Trojan": -150, #чистый. «ковровая» блокировка
                "VLESS": -150, #чистый. «ковровая» блокировка
                "VMess": -150, #чистый. «ковровая» блокировка
                "Hysteria": -150, #«ковровая» блокировка
                "Hysteria2": -150, #«ковровая» блокировка
                "QUIC": -150, #«ковровая» блокировка
                "TUIC": -150, #«ковровая» блокировка
                "NaiveProxy": 0, #нет информации
                "SSH Tunnel": -200, #Обнаруживаются легко
                "MTProto Proxy": 0 #нет информации
            })
            calcul_result()
            print("Применён профиль")

def Selecting_mode():
    global current_mode
    global mode_scores
    utils.clear_terminal()
    print(Selecting_mode_menu)
    choice = input("Введите в этом поле: ")
    if not choice.isdigit():
        print("Нужно ввести число")
        return
    mode = int(choice)
    if mode == 0:
        return
    
    if mode == 1:
        #игровой режим
        if current_mode != 1:
            mode_scores.update({
                "OpenVPN": -30, #тяжелее и медленнее
                "WireGuard": 100, #низкая задержка
                "AmneziaWG": 100, # WG + маскеровка
                "Lightway": 0, # я хз
                "SoftEther": -100, # для обхода создан
                "IKEv2/IPSec": 0, # я хз
                "SSTP": -200, # медленный, только на win и то после некоторое время сам выключался или же TCP поверх TCP - боль
                "SOCKS5": 0, # я хз
                "HTTP Proxy": 0, # я хз
                "Shadowsocks": 0, # я хз
                "Trojan": 0, # я хз
                "VLESS": -40, # играть можно но на костылях, т. к. обход важнее задержки
                "VMess": -80, # староват и тяжелее
                "Hysteria": 100, # хорош при потерях
                "Hysteria2": 100, # тот же хисткрия, только новее
                "QUIC": 0, # хз
                "TUIC": 0, # хз
                "NaiveProxy": 0, # хз
                "SSH Tunnel": 0, # хз
                "MTProto Proxy": 0 # он для телеграма создан, так что 0 
            })

            current_mode = 1
            calcul_result()
            print("Приоретет изменён, смотрити в 'список прироритетных протоколов' ")
            print(current_mode)
            return
        else:
            print("в данном моменте вы используете этот режим ")
            return 
        
    if mode == 2:
        #Режим борщивика
        if current_mode != 2:
            mode_scores.update({
                "OpenVPN": -150, #некоторые DPI знает характер
                "WireGuard": -150, #некоторые DPI знает характер
                "AmneziaWG": 100, # WG + маскировка
                "Lightway": 0, # я хз
                "SoftEther": 100, # для обхода создан
                "IKEv2/IPSec": 0, # я хз
                "SSTP": -10, # для временного захода сойдёт
                "SOCKS5": 0, # я хз
                "HTTP Proxy": 0, # я хз
                "Shadowsocks": 50, # как раз для этого, но в некоторых стран уже блокируется
                "Trojan": 50, # как раз для этого, но думаю, если не правильно настроить, то лекго обноружить
                "VLESS": 150, # как раз для этого создан
                "VMess": 100, # как атернативный вариант VLESS
                "Hysteria": 100, # хорош при потерях
                "Hysteria2": 100, # тот же хисткрия, только новее
                "QUIC": 0, # хз
                "TUIC": 0, # хз
                "NaiveProxy": 0, # хз
                "SSH Tunnel": 0, # хз
                "MTProto Proxy": 50 # для телеграмма он создан, но он основывается на SS, да и щас легко палится
                })
             
            current_mode = 2
            calcul_result()
            print("Приоретет изменён, смотрити в 'список прироритетных протоколов' ")
            print(current_mode)
            return
        else:
            print("в данном моменте вы используете этот режим ")
            return  

    if mode == 3:
        #Режим шпиона
        if current_mode != 3:
            mode_scores.update ({
                "OpenVPN": -150, #некоторые DPI знает характер
                "WireGuard": -150, #некоторые DPI знает характер
                "AmneziaWG": 100, # WG + маскировка
                "Lightway": 0, # я хз
                "SoftEther": 50, # для обхода создан, но он тяжёлый
                "IKEv2/IPSec": 0, # я хз
                "SSTP": -100, # для временного захода сойдёт
                "SOCKS5": 0, # я хз
                "HTTP Proxy": 0, # я хз
                "Shadowsocks": 50, # как раз для этого, но в некоторых стран уже блокируется
                "Trojan": 50, # как раз для этого, но думаю, если не правильно настроить, то лекго обноружить
                "VLESS": 150, # как раз для этого создан
                "VMess": 100, # как атернативный вариант VLESS
                "Hysteria": 100, # хорош при потерях
                "Hysteria2": 100, # тот же хисткрия, только новее
                "QUIC": 0, # хз
                "TUIC": 0, # хз
                "NaiveProxy": 0, # хз
                "SSH Tunnel": 0, # хз
                "MTProto Proxy": 50 # для телеграмма он создан, но он основывается на SS, да и щас легко палится
            })

            current_mode = 3
            calcul_result()
            print("Приоретет изменён, смотрити в 'список прироритетных протоколов' ")
            print(current_mode)
            return
        else:
            print("в данном моменте вы используете этот режим ")
            return  

    if mode == 4:
        #Режим агента
        if current_mode != 4:
            # Пришлось Чату GPT попросить, т. к. для меня стабильность -- анти-DPI протокол или его провайдер не отвалился за 3 дня
            mode_scores.update ({
                "OpenVPN": 20,         # старый, тяжёлый, но зрелый и предсказуемый
                "WireGuard": 100,      # простой, быстрый, стабильный
                "AmneziaWG": 80,       # WG + маскировка, чуть сложнее обычного WG
                "Lightway": 0,         # мало данных
                "SoftEther": -20,      # мощный, но сложнее и не самый лёгкий
                "IKEv2/IPSec": 40,     # стабильный мобильный вариант, но зависит от сети
                "SSTP": -80,           # TCP/TLS, может быть медленным и тяжёлым
                "SOCKS5": 0, # я хз
                "HTTP Proxy": -50,     # не универсален, не полноценный VPN
                "Shadowsocks": 20,     # простой прокси, может быть стабильным при нормальной сети
                "Trojan": 30,          # может быть стабильным при хорошей настройке TLS
                "VLESS": 40,           # гибкий, но качество сильно зависит от конфига
                "VMess": -20,          # старее и тяжелее VLESS
                "Hysteria": 30,        # хорош при потерях, но UDP/QUIC может быть нестабилен в некоторых сетях
                "Hysteria2": 40,       # новее Hysteria, полезен при плохих сетях
                "QUIC": 0, # хз
                "TUIC": 20,            # QUIC-based, потенциально хорошо, но зависит от сети
                "NaiveProxy": 10,      # может выглядеть как обычный HTTPS, но не универсален
                "SSH Tunnel": -30,     # простой, но не лучший для постоянного транспорта
                "MTProto Proxy": -100, # специализирован под Telegram, не общий стабильный транспорт
            })

            current_mode = 4
            calcul_result()
            print("Приоретет изменён, смотрити в 'список прироритетных протоколов' ")
            print(current_mode)
            return
        else:
            print("в данном моменте вы используете этот режим ")
            return  


    if mode == 5:
        print("Для этой версии программы не работает")
        return
    
def calcul_result():
    global final_score
    global base_scores 
    global blocked_scores 
    global mode_scores 
    for protocol in protocols:
        if blocked_scores[protocol] <= -200:
            final_score[protocol] = -200
        else:
            total = (
                base_scores[protocol]
                + mode_scores[protocol]
                + blocked_scores[protocol]
            )

            final_score[protocol] = clamp_score(total)

def menu():
    while True:
        global final_score
        global base_scores 
        global blocked_scores 
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
            for protocol, score in base_scores.items():
                print(f"{protocol:15} : {score:+4}")
            print("----------------------------------")
            print("Заблокированные протоколы")
            for protocol, score in blocked_scores.items():
                print(f"{protocol:15} : {score:+4}")
            print("----------------------------------")
            print("Режим")
            for protocol, score in mode_scores.items():
                print(f"{protocol:15} : {score:+4}")
            print("----------------------------------")
            print("Итог (сумма по умолчанию, заблокированых протоколов, режим и по сортировки лучший --> худший)")
            calcul_result()
            sorted_final = sorted(
                final_score.items(),
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