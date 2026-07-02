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
    "QUIC",
    "TUIC", 
    "NaiveProxy", 
    "SSH Tunnel", 
    "MTProto Proxy"
    ]

regions = {
    "Нидерланды": [
        "Amsterdam",
        "Rotterdam",
        "Eindhoven"
    ],

    "Германия": [
        "Frankfurt",
        "Berlin",
        "Munich",
        "Hamburg"
    ],

    "Швейцария": [
        "Zurich",
        "Geneva"
    ],

    "Финляндия": [
        "Helsinki"
    ],

    "Швеция": [
        "Stockholm",
        "Gothenburg"
    ],

    "Польша": [
        "Warsaw",
        "Kraków",
        "Poznań"
    ],

    "Япония": [
        "Tokyo",
        "Osaka"
    ],

    "Россия": [
        "Moscow",
        "Saint Petersburg",
        "Novosibirsk"
    ],

    "Турция": [
        "Istanbul",
        "Ankara"
    ],

    "ОАЭ": [
        "Dubai",
        "Abu Dhabi"
    ],

    "Казахстан": [
        "Almaty",
        "Astana"
    ],

    "Сингапур": [
        "Singapore"
    ],

    "Австралия": [
        "Sydney",
        "Melbourne",
        "Perth",
        "Brisbane"
    ],

    "Франция": [
        "Paris",
        "Marseille",
        "Lyon"
    ]
}

#не активный, но на будущее
servers = {
    "Германия": {
        "cities": [
            "Frankfurt",
            "Berlin",
            "Munich"
        ],
        "dpi": False,
        "udp_block": False
    },

    "Россия": {
        "cities": [
            "Moscow",
            "Saint Petersburg"
        ],
        "dpi": True,
        "udp_block": False
    }
}
#servers = {
#    "Германия": {
#        "cities": [...],
#        "providers": [
#            "Hetzner",
#            "OVH",
#            "DigitalOcean"
#        ],
#        "dpi": False,
#        "quic_block": False,
#        "wireguard_detect": False
#    }
#}

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
    clear_terminal()
    # Ping в мс (RTT (Round Trip Time) -- пользователь говорит, сервер отвечает)
    # Latency в мс (Пользователь говорит серверу) сложное в реализации
    # Jitter в мс (скачки пинга)
    # Packet Loss в % (потери)
    # Bandwidth в Мбит/с (скорость)
    if random.random() < 0.70:
        ping_ms_tcp = random.randint(20, 100)
    elif random.random() < 0.90:
        ping_ms_tcp = random.randint(100, 300)
    elif random.random() < 0.98:
        ping_ms_tcp = random.randint(300, 600)
    else:
        ping_ms_tcp = random.randint(600, 1000)
    
    if random.random() < 0.8:
        loss = random.uniform(0, 1)
    elif random.random() < 0.95:
        loss = random.uniform(1, 5)
    else:
        loss = random.uniform(5, 20)

    if random.random() < 0.75:
        jitter = random.randint(0, 5)
    elif random.random() < 0.95:
        jitter = random.randint(5, 20)
    else:
        jitter = random.randint(20, 80)
    
    if random.random() < 0.7:
        cpu = random.randint(10, 60)
    elif random.random() < 0.9:
        cpu = random.randint(60, 85)
    else:
        cpu = random.randint(85, 100)

#100–1000+ Мбит/с - отлично
#30–100 Мбит/с - нормально
#5–30 Мбит/с - плохо
#<5 Мбит/с - очень плохо
    if random.random() < 0.65:
        Download = random.randint(100, 2500)
    elif random.random() < 0.85:
        Download = random.randint(30, 100)
    elif random.random() < 0.97:
        Download = random.randint(5, 30)
    else:
        Download = random.randint(1, 5)

#50–500+ Мбит/с - отлично
#10–50 Мбит/с - нормально
#2–10 Мбит/с - плохо
#<2 Мбит/с - очень плохо
    if random.random() < 0.65:
        upload = random.randint(50, 1500)
    elif random.random() < 0.85:
        upload = random.randint(10, 50)
    elif random.random() < 0.97:
        upload = random.randint(2, 10)  
    else:
        upload = random.randint(1, 9)

    country = random.choice(list(regions.keys()))
    city = random.choice(regions[country])

    dpi_detector = random.random() > 0.5
    
    print("ID: [В данном моменте не используется]")
    print(f"Пинг: {ping_ms_tcp} мс по TCP")
    print(f"Искажение/дрожание: {jitter} мс")
    print(f"Потеря пакетов: {loss:.2f}%")
    print(f"Скачивание: {Download} Мбит/с" )
    print(f"Загрузки: {upload} Мбит/с" )
    print(f"CPU/разгрузка сервера: {cpu}%")
    print(f"Страна и город: {country}, {city}")
    print("Поддерживаемый протокол: [по умолчанию все]" )
    print("Обнаруживает DPI?:", dpi_detector)

def block_protocol_menu():
    #Регион / Провайдер
    #DPI
    #UDP Block
    #QUIC Block
    #WireGuard Detection
    #OpenVPN Detection
    #VLESS Detection
    
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


Selecting_mode_menu = """
---------------------------------
Выберите режим
---------------------------------

1. Игровой: для стабильной игры
2. Обход методом Heracleum: обход любой ценой
3. Обход методом Шпиона: обход + стабильность
4. Агент: стабильность
5. Авто: Алгоритм сам выбирает (Для этой версии программы не работает)
---------------------------------
0 -- Выход
"""

menu_text = """
---------------------------------
Песочница сети
---------------------------------

1 -- создать псевдорандомный сервер (щас это просто кликер)
2 -- регион обнаруживает/блокирует протокол
3 -- показать список серверов
4 -- список протоколов и технологий
5 -- список приоритетных протоколов
6 -- Выбор режима и методом ATE
7 -- Симуляция деградации сети (недоступно)

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
QUIC
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
Что обнаруживает/блокирует?
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
16. QUIC
17. TUIC
18. NaiveProxy
19. SSH Tunnel
20. MTProto Proxy (протокол для Телеграма)
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

