import random
import os

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

# QUIT можешь добавить
# Latency (пинг)
# Jitter (скачки пинга)
# Packet Loss (потери)
# Bandwidth (скорость)

#для оценки:
#100  = рекомендую
#50   = скорее хорошо
#0    = неизвестно/нейтрально
#-50  = скорее плохо
#-100 = плохо
#-200 = почти исключить



MIN_SCORE = -200
MAX_SCORE = 200

def clamp_score(value):
    return max(MIN_SCORE, min(MAX_SCORE, value))


def clear_terminal():
    if os.name == "nt":
        os.system("cls")

    else:
        os.system("clear")


def generate_server_stats():
    #r = random.random()
    #if r < 0.70:
    #    ping_ms_tcp = random.randint(20, 100)
    #elif r < 0.90:
    #    ping_ms_tcp = random.randint(100, 300)
    #elif r < 0.98:
    #    ping_ms_tcp = random.randint(300, 600)
    #else:
    #    ping_ms_tcp = random.randint(600, 1000)

    if random.random() < 0.8:
        ping_ms_tcp = random.randint(10, 150)
    else:
        ping_ms_tcp = random.randint(150, 1000)
    #Нидералнд, Германия, Швейцария, Финлядия, Шведция, Польша, Япония, Россия, Турция, ОАЭ, Казахстан, Сингапур, Австралия
    loss = random.randrange(100)
    dpi_detector = random.random() > 0.5

    print("Пинг в мс по TCP:", ping_ms_tcp)
    print("Потеря пакетов:", loss, "%")
    print("Находиться в ЧС у DPI?:", dpi_detector)

def block_protocol_menu():
    global blocked_scores
    clear_terminal()
    print(menu_block)
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

def Selecting_mode():
    global current_mode
    global mode_scores
    clear_terminal()
    print(Selecting_mode_menu)
    choice = input("Введите в этом поле: ")
    if not choice.isdigit():
        print("Нужно ввести число")
        return
    mode = int(choice)
    if mode == 0:
        return
    
    if mode == 1:
        if current_mode != 1:
            mode_scores.update({
                "OpenVPN": -30, #тяжелее и медленнее
                "WireGuard": 100, #низкая задержка
                "AmneziaWG": 100, # WG + маскеровка
                "Lightway": 0, # я хз
                "SoftEther": -100, # для обхода создан
                "IKEv2/IPSec": 0, # я хз
                "SSTP": -200, # медленный, только на win и то после некоторое время сам выключался или же TCP поверх TCP - боль
                "HTTP Proxy": 0, # я хз
                "Shadowsocks": 0, # я хз
                "Trojan": 0, # я хз
                "VLESS": -40, # играть можно но на костылях, т. к. обход важнее задержки
                "VMess": -80, # староват и тяжелее
                "Hysteria": 100, # хорош при потерях
                "Hysteria2": 100, # тот же хисткрия, только новее
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
        if current_mode != 2:
            mode_scores.update({
                "OpenVPN": -150, #некоторые DPI знает характер
                "WireGuard": -150, #некоторые DPI знает характер
                "AmneziaWG": 100, # WG + маскировка
                "Lightway": 0, # я хз
                "SoftEther": 100, # для обхода создан
                "IKEv2/IPSec": 0, # я хз
                "SSTP": -10, # для временного захода сойдёт
                "HTTP Proxy": 0, # я хз
                "Shadowsocks": 50, # как раз для этого, но в некоторых стран уже блокируется
                "Trojan": 50, # как раз для этого, но думаю, если не правильно настроить, то лекго обноружить
                "VLESS": 150, # как раз для этого создан
                "VMess": 100, # как атернативный вариант VLESS
                "Hysteria": 100, # хорош при потерях
                "Hysteria2": 100, # тот же хисткрия, только новее
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
        if current_mode != 3:
            # Пришлось Чату GPT попросить, т. к. для меня стабильность -- анти-DPI протокол или его провайдер не отвалился за 3 дня
            mode_scores.update ({
                "OpenVPN": 20,         # старый, тяжёлый, но зрелый и предсказуемый
                "WireGuard": 100,      # простой, быстрый, стабильный
                "AmneziaWG": 80,       # WG + маскировка, чуть сложнее обычного WG
                "Lightway": 0,         # мало данных
                "SoftEther": -20,      # мощный, но сложнее и не самый лёгкий
                "IKEv2/IPSec": 40,     # стабильный мобильный вариант, но зависит от сети
                "SSTP": -80,           # TCP/TLS, может быть медленным и тяжёлым
                "HTTP Proxy": -50,     # не универсален, не полноценный VPN
                "Shadowsocks": 20,     # простой прокси, может быть стабильным при нормальной сети
                "Trojan": 30,          # может быть стабильным при хорошей настройке TLS
                "VLESS": 40,           # гибкий, но качество сильно зависит от конфига
                "VMess": -20,          # старее и тяжелее VLESS
                "Hysteria": 30,        # хорош при потерях, но UDP/QUIC может быть нестабилен в некоторых сетях
                "Hysteria2": 40,       # новее Hysteria, полезен при плохих сетях
                "TUIC": 20,            # QUIC-based, потенциально хорошо, но зависит от сети
                "NaiveProxy": 10,      # может выглядеть как обычный HTTPS, но не универсален
                "SSH Tunnel": -30,     # простой, но не лучший для постоянного транспорта
                "MTProto Proxy": -100, # специализирован под Telegram, не общий стабильный транспорт
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


Selecting_mode_menu = """
---------------------------------
Выберите режим
---------------------------------

1. Игровой
2. обход 
3. агент 
4. авто (Для этой версии программы не работает)
---------------------------------
0 -- Выход
"""

menu_text = """
---------------------------------
Песочница сети
---------------------------------

1 -- создать псевдорандомный сервер (щас это просто кликер)
2 -- регион блокирует протокол
3 -- показать список серверов
4 -- Список протоколов и технологий
5 -- список приоритетных протоколов
6 -- Выбор режима ATE: Игровой, обход, агент, авто
7 -- Симуляция деградации сети (недоступно)
Типо: packet loss вырос; ping скачет; throttling.

---------------------------------
0 -- выход
"""
list_protocol = """
----------------------------------
Список протоколов и технологий
----------------------------------
VPN

OpenVPN
WireGuard
AmneziaWG
Lightway
SoftEther (SSL-VPN)
IKEv2/IPSec
SSTP
----------------------------------
Proxy / Tunnel Protocols

SOCKS5
HTTP Proxy
Shadowsocks
Trojan
VLESS
VMess
Hysteria
Hysteria2
TUIC
NaiveProxy
SSH Tunnel
MTProto Proxy (протокол для Телеграма)
----------------------------------
Транспорты

TCP
UDP
QUIC
HTTP/2
HTTP/3
WebSocket (WS)
WebSocket Secure (WSS)
gRPC
xHTTP
KCP
DomainSocket
----------------------------------
Методы обфускации / маскировки

TLS
REALITY
uTLS
FakeTLS
Padding
Fragmentation
SNI Spoofing
Domain Fronting
CDN masking
Randomized packets
XTLS
Obfs4
----------------------------------
Ядра / Движки

Xray-core
Sing-box
Clash.Meta
OpenVPN core
WireGuard tools
Hysteria core
SoftEther server/client

---------------------------------
Оценка для (В данном моменте не используется)

Игр
Обхода
Стриминги
Стабильности
Меньшего задержек
Не обнаружаемости 
меньшего нагрузки (слабый компьютер и телефон)
"""


menu_block = """
---------------------------------
Что блокируется?
---------------------------------
VPN

1. OpenVPN
2. WireGuard
3. AmneziaWG
4. Lightway
5. SoftEther (SSL-VPN)
6. IKEv2/IPSec
7. SSTP
----------------------------------
Proxy / Tunnel Protocols

8. SOCKS5
9. HTTP Proxy
10. Shadowsocks
11. Trojan
12. VLESS
13. VMess
14. Hysteria
15. Hysteria2
16. TUIC
17. NaiveProxy
18. SSH Tunnel
19. MTProto Proxy (протокол для Телеграма)
----------------------------------
0. Выход
"""



def menu():
    while True:
        global final_score
        global base_scores 
        global blocked_scores 
        global mode_scores
        clear_terminal()
        print(menu_text)
        choice = input("Введите в этом поле: ")

        if not choice.isdigit():
            print("Нужно ввести число")
            input("\nНажми Enter...")
            continue

        x = int(choice)

        if x == 1:
            generate_server_stats()
        elif x == 2:
            block_protocol_menu()
        elif x == 3:
            pass
        elif x == 4:
            clear_terminal()
            print(list_protocol)
        elif x == 5:
            clear_terminal()
            print("по умолчанию")
            print(base_scores)
            print("Заблокированные протоколы")
            print(blocked_scores)
            print("Режим")
            print(mode_scores)
            print("Итог (сумма по умолчанию, заблокированых протоколов и режим)")
            print(clamp_score)
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

