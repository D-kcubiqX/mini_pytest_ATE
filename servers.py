import random
import utils
import json
import os
SERVERS_FILE = "servers.json"

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
    ],

    "Испания": [
        "Madrid",
        "Barcelona"
    ]
}

labels = {
    "id": "ID",
    "country": "Страна",
    "city": "Город",
    "ping": "Пинг",
    "jitter": "Jitter",
    "packet_loss": "Потери",
    "download": "Скачивание",
    "upload": "Загрузка",
    "cpu": "CPU"
}

units = {
    "ping": "мс",
    "jitter": "мс",
    "packet_loss": "%",
    "download": "Мбит/с",
    "upload": "Мбит/с",
    "cpu": "%"
}

#не активный, но на будущее
#servers = {
#    "Германия": {
#        "cities": [
#            "Frankfurt",
#            "Berlin",
#            "Munich"
#        ],
#        "dpi": False,
#        "udp_block": False
#    },
#
#    "Россия": {
#        "cities": [
#            "Moscow",
#            "Saint Petersburg"
#        ],
#        "dpi": True,
#        "udp_block": False
#    }
#}

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

def load_servers():
    if not os.path.exists(SERVERS_FILE):
        return []

    with open(SERVERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    
def save_servers(servers):
    with open(SERVERS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            servers,
            file,
            ensure_ascii=False,
            indent=4
        )

def generate_server_id(servers):
    numbers = []

    for server in servers:
        number = int(server["id"].replace("srv-", ""))
        numbers.append(number)

    next_number = max(numbers, default=0) + 1
    return f"srv-{next_number:04d}"

def create_and_save_server():
    saved_servers = load_servers()

    server = generate_server()
    server["id"] = generate_server_id(saved_servers)

    saved_servers.append(server)
    save_servers(saved_servers)

    print(f"Сервер {server['id']} сохранён.")

def show_servers():
    saved_servers = load_servers()

    if not saved_servers:
        print("Сохранённых серверов нет.")
        return

    for server in saved_servers:
        for key, value in server.items():
            if key in units:
                print(f"{labels[key]}: {value} {units[key]}")
            else:
                print(f"{labels[key]}: {value}")

def generate_server():
    utils.clear_terminal()
    # Ping в мс (RTT (Round Trip Time) -- пользователь говорит, сервер отвечает)
    # Latency в мс (Пользователь говорит серверу) сложное в реализации
    # Bandwidth в Мбит/с (скорость)

    
    if random.random() < 0.70:
        ping_ms_tcp = random.randint(20, 100)
    elif random.random() < 0.90:
        ping_ms_tcp = random.randint(100, 300)
    elif random.random() < 0.98:
        ping_ms_tcp = random.randint(300, 600)
    else:
        ping_ms_tcp = random.randint(600, 1000)
    
    # Packet Loss в % (потери)
    if random.random() < 0.8:
        loss = random.uniform(0, 1)
    elif random.random() < 0.95:
        loss = random.uniform(1, 5)
    else:
        loss = random.uniform(5, 20)

    # Jitter в мс (скачки пинга)
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
        download_speed = random.randint(100, 2500)
    elif random.random() < 0.85:
        download_speed = random.randint(30, 100)
    elif random.random() < 0.97:
        download_speed = random.randint(5, 30)
    else:
        download_speed = random.randint(1, 5)

#50–500+ Мбит/с - отлично
#10–50 Мбит/с - нормально
#2–10 Мбит/с - плохо
#<2 Мбит/с - очень плохо
    if random.random() < 0.65:
        upload_speed = random.randint(50, 1500)
    elif random.random() < 0.85:
        upload_speed = random.randint(10, 50)
    elif random.random() < 0.97:
        upload_speed = random.randint(2, 10)  
    else:
        upload_speed = random.randint(1, 9)

    country = random.choice(list(regions.keys()))
    city = random.choice(regions[country])

    dpi_detector = random.random() > 0.5

    #protocol_count = random.randint(3, 8)

    #supported_protocols = random.sample(
    #    protocols,
    #    k=protocol_count
    #)
    server = {
        "id": "srv-0001",
        "country": country,
        "city": city,
        "ping": ping_ms_tcp,
        "jitter": jitter,
        "packet_loss": round(loss, 2),
        "download": download_speed,
        "upload": upload_speed,
        "cpu": cpu,
    #    "protocols": supported_protocols
    }

    print(f"Пинг: {ping_ms_tcp} мс по TCP")
    print(f"Искажение/дрожание: {jitter} мс")
    print(f"Потеря пакетов: {loss:.2f}%")
    print(f"Скачивание: {download_speed} Мбит/с" )
    print(f"Загрузки: {upload_speed} Мбит/с" )
    print(f"CPU/разгрузка сервера: {cpu}%")
    print(f"Страна и город: {country}, {city}")
    print("Поддерживаемый протокол: [по умолчанию все]" )
    print("Обнаруживает DPI?:", dpi_detector)

    return server
    

#server_id = input("Введите ID сервера: ")

#for server in servers:
#    if server["id"] == server_id:
#        server["ping"] = int(input("Новый ping: "))
#        break
#else:
#    print("Сервер не найден")

#import json

#with open("servers.json", "r", encoding="utf-8") as file:
#    servers = json.load(file)

#def calculate_server_score(server):
#    score = 0
#
#    score -= server["ping"]
#    score -= server["jitter"] * 2
#    score -= server["packet_loss"] * 20
#    score -= server["cpu"] * 0.5
#    score += server["download"] * 0.05
#    score += server["upload"] * 0.03
#
#    return score
#best_server = max(servers, key=calculate_server_score)

