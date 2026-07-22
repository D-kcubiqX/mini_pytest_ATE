from protocols import protocols
from scores import region_scores, calcul_result, mode_scores, manual_scores, clamp_score
from texts import menu_block, menu_block_protocol, menu_block_profile, Selecting_mode_menu
from protocol_profiles import profiles
import utils

current_mode = 0

def block_protocol_menu():
    #Регион / Провайдер
    #DPI
    #UDP Block
    #QUIC Block
    #WireGuard Detection
    #OpenVPN Detection
    #VLESS Detection
    global region_scores
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
        global region_scores
        global manual_scores
        utils.clear_terminal()
        print(menu_block_protocol)
        #choice = input("Введите в этом поле: ")
        protocol_number = int(input("Выберите протокол: "))
        #if not protocol_number.isdigit():
        #    print("Нужно ввести число")
        if protocol_number >= len(protocols):
            print("Такого протокола нет")
        else:
            protocol = protocols[protocol_number - 1]
            new_score = int(input("""Введите оценку от -200 до 200, где -200 -- почти или полностью исключить, а 200 -- настоятельно рекомендую. 0 -- нейтральный/сброс: """))
            manual_scores[protocol] = clamp_score(new_score)
            print(f"Очки {protocol} теперь: {manual_scores[protocol]}")
            calcul_result()

        if protocol_number == 0:
            return

        #    return
        #protocol_block = int(choice)
        #if protocol_block == 0:
        #    return
        #if 1 <= protocol_block <= len(protocols):
        #    blocked_protocol = protocols[protocol_block - 1]
        #    print("Регион блокирует:", blocked_protocol)
        #    manual_scores[blocked_protocol] = -200
        #    calcul_result()
        #    print("Очки протокола теперь:", manual_scores[blocked_protocol])
    if mb_choice1 == 2:
        for protocol in protocols:
            manual_scores[protocol] = 0
        calcul_result()
        print("приорететы сброшены")

    if mb_choice1 == 3:
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
            region_scores.update(profiles["Россия"])
            calcul_result()
            print("Применён профиль")

        if profile_block == 2:
            region_scores.update(profiles["Китай"])
            calcul_result()
            print("Применён профиль")
            
        if profile_block == 3:
            region_scores.update(profiles["Туркменистан"])
            calcul_result()
            print("Применён профиль")

        if profile_block == 4:
            region_scores.update(profiles["Иран"])
            calcul_result()
            print("Применён профиль")
    if mb_choice1 == 4:
            for protocol in protocols:
                region_scores[protocol] = 0
            calcul_result()
            print("Профиль сброшены")
    
    if mb_choice1 == 5:
        for protocol in protocols:
            region_scores[protocol] = 0
            manual_scores[protocol] = 0
        calcul_result()
        print("Профиль и приорететы сброшены")

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