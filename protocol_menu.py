from protocols import protocols
from scores import region_scores, calcul_result, mode_scores, manual_scores, clamp_score, base_scores, final_score, target_scores
from texts import menu_block_protocol, menu_block_profile, profil_region_menu, Selecting_mode_menu, Selecting_target_menu
from protocol_profiles import profiles
import utils

current_mode = 1
current_target = 1

#def block_protocol_menu():
    #Регион / Провайдер
    #DPI
    #UDP Block
    #QUIC Block
    #WireGuard Detection
    #OpenVPN Detection
    #VLESS Detection

def priority_protocol_tech():
    utils.clear_terminal()
    print("по умолчанию")
    for protocol, score in base_scores.items():
        print(f"{protocol:15} : {score:+4}")
    print("----------------------------------")
    print("Региональная оценка")
    for protocol, score in region_scores.items():
        print(f"{protocol:15} : {score:+4}")
    print("----------------------------------")
    print("Пользовательский настройка")
    for protocol, score in manual_scores.items():
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

def Profil_region():
    global region_scores
    utils.clear_terminal()
    print(profil_region_menu)
    choice = utils.digit_checker()

    if choice == None:
        input("\nНажми Enter...")
        pass

    if choice == 0:
        return
    if choice == 1:
        global region_scores
        print(menu_block_profile)
        profiles_choice = utils.digit_checker()
        if profiles_choice == 0:
            return
        if profiles_choice == 1:
            region_scores.update(profiles["Россия"])
            calcul_result()
            print("Применён профиль")

        if profiles_choice == 2:
            region_scores.update(profiles["Китай"])
            calcul_result()
            print("Применён профиль")
            
        if profiles_choice == 3:
            region_scores.update(profiles["Туркменистан"])
            calcul_result()
            print("Применён профиль")

        if profiles_choice == 4:
            region_scores.update(profiles["Иран"])
            calcul_result()
            print("Применён профиль")
    if choice == 2:
        for protocol in protocols:
            region_scores[protocol] = 0
        calcul_result()
        print("Профиль сброшены")

def manual_setting():
    global manual_scores
    utils.clear_terminal()
    print(profil_region_menu)
    choice = utils.digit_checker()
    if choice == 0:
        return
    if choice == 1:
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
    if choice == 2:
        for protocol in protocols:
            manual_scores[protocol] = 0
        calcul_result()
        print("приорететы сброшены")        

def Selecting_target():
    global current_target
    global target_scores
    utils.clear_terminal()
    print(Selecting_target_menu)
    target = utils.digit_checker()
    if target == 0:
        return
    if target == 1:
        if current_mode != 1:
            for protocol in protocols:
                target_scores[protocol] = 0        
    if target == 2:
        if current_target != 2:
            target_scores.update({
                "OpenVPN": -50, #условно т.к есть UDP (50) и TCP (-100)
                "WireGuard": 150,
                "AmneziaWG": 120,
                "Lightway": 120,
                "SoftEther": 0, # для обхода создан, а так хз
                "IKEv2/IPSec": 80,
                "SSTP": -100,
                "SOCKS5": 20,
                "HTTP Proxy": -50,
                "Shadowsocks": 80,
                "Trojan": 40,
                "VLESS": 80,
                "VMess": 30,
                "Hysteria": 120,
                "Hysteria2": 150,
                "QUIC": 0, # неизвестно
                "TUIC": 150,
                "NaiveProxy": -20,
                "SSH Tunnel": -100,
                "MTProto Proxy": -100
                })
             
            current_target = 2
            calcul_result()
            print("цель изменён, смотрити в 'список прироритетных протоколов' ")
            print(current_target)
            return
        else:
            print("в данном моменте вы используете этот цель ")
            return          
    if target == 3:
        if current_target != 3:
            target_scores.update({
                "OpenVPN": 60, #условно т.к есть UDP (80) и TCP (20)
                "WireGuard": 120,
                "AmneziaWG": 100,
                "Lightway": 120,
                "SoftEther": 60,
                "IKEv2/IPSec": 100,
                "SSTP": 20,
                "SOCKS5": 50,
                "HTTP Proxy": 30,
                "Shadowsocks": 100,
                "Trojan": 100,
                "VLESS": 100,
                "VMess": 80,
                "Hysteria": 130,
                "Hysteria2": 150,
                "QUIC": 0, # неизвестно
                "TUIC": 140,
                "NaiveProxy": 80,
                "SSH Tunnel": -20,
                "MTProto Proxy": -100
                })
             
            current_target = 3
            calcul_result()
            print("цель изменён, смотрити в 'список прироритетных протоколов' ")
            print(current_target)
            return
        else:
            print("в данном моменте вы используете этот цель ")
            return

    if target == 4:
        if current_target != 4:
            target_scores.update({
                "OpenVPN": 80, #условно т.к есть UDP (100) и TCP (80)
                "WireGuard": 120,
                "AmneziaWG": 100,
                "Lightway": 100,
                "SoftEther": 100,
                "IKEv2/IPSec": 120,
                "SSTP": 80,
                "SOCKS5": 50,
                "HTTP Proxy": 40,
                "Shadowsocks": 80,
                "Trojan": 100,
                "VLESS": 100,
                "VMess": 80,
                "Hysteria": 80,
                "Hysteria2": 100,
                "QUIC": 0, # неизвестно
                "TUIC": 100,
                "NaiveProxy": 100,
                "SSH Tunnel": 100,
                "MTProto Proxy": 0
                })
             
            current_target = 4
            calcul_result()
            print("цель изменён, смотрити в 'список прироритетных протоколов' ")
            print(current_target)
            return
        else:
            print("в данном моменте вы используете этот цель ")
            return
    
    if target == 5:
        print("Для этой версии программы не работает")
        return


#| Протокол      | Игры | Стриминг | Работа |
#| ------------- | ---: | -------: | -----: |
#| OpenVPN UDP   |  +50 |      +80 |   +100 |
#| OpenVPN TCP   | -100 |      +20 |    +80 |



def Selecting_mode():
    global current_mode
    global mode_scores
    utils.clear_terminal()
    print(Selecting_mode_menu)
    mode = utils.digit_checker()
    if mode == 0:
        return
    
    if mode == 1:
        #Без режима
        if current_mode != 1:
            for protocol in protocols:
                mode_scores[protocol] = 0

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