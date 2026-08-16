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


# Transport -- TCP, UDP, QUIC, KCP
# Transport Security -- TLS XTLS uTLS

# Encapsulation:
# HTTP/2 (Инкапсулируется в TCP сегменты)
# HTTP/3 (Инкапсулируется в QUIC (который инкапсулирован в UDP))
# WebSocket (Инкапсулируется в TCP сегменты (начинается как HTTP-запрос))
# gRPC (Инкапсулируется в HTTP/2, а затем в TCP)
# xHTTP (Инкапсулируется в TCP или другие кастомные транспорты)

# Obfuscation:
# Имитация легитимного трафика (Stealth & Mimicry) -- REALITY, FakeTLS (МТпрокси используется, но обнаружается), Obfs4 
# Манипуляция маршрутом и инфраструктурой (Routing & Masking) -- CDN masking, Domain Fronting (закрыто уязвимость)
# Манипуляция метаданными и заголовками (Header Modification) -- SNI Spoofing
# Обман DPI на уровне пакетов (Packet-Level Manipulation) -- Fragmentation, Padding, Randomized packets

# gRPC / HTTP (Прикладной уровень)
# инкапсулируется в TLS / XTLS (Шифрование данных и маскировка)
# инкапсулируется в TCP / UDP / QUIC (транспортный уровень)
# инкапсулируется в IP (Сетевой уровень)



#Transport_protocols = [
#    "TCP",
#    "UDP",
#    "QUIC",
#    "HTTP/2",
#    "HTTP/3",
#    "WebSocket",
#    "WebSocket Secure",
#    "gRPC",
#    "xHTTP",
#    "KCP",
#    "DomainSocket"
#]

#Obfuscation = [
#    "TLS",
#    "REALITY",
#    "uTLS",
#    "FakeTLS",
#    "Padding",
#    "Fragmentation",
#    "SNI Spoofing",
#    "Domain Fronting",
#    "CDN masking",
#    "Randomized packets",
#    "XTLS",
#    "Obfs4"
#]





technologies = {
    "OpenVPN": {
        "category": "VPN",
        "transports": ["TCP", "UDP"],
        "security": ["TLS"],
        "obfuscation": None,
    },

    "Hysteria2": {
        "category": "Proxy",
        "transports": ["QUIC", "UDP"],
        "security": ["TLS"],
        "obfuscation": ["Salamander", "Gecko"],
    },

    "TUIC": {
        "category": "Proxy",
        "transports": ["QUIC", "UDP"],
        "security": ["TLS"],
        "obfuscation": [],
    },

    "NaiveProxy": {
        "category": "Proxy",
        "transports": ["HTTP/2", "HTTP/3"],
        "security": ["TLS"],
        "obfuscation": [
            "Padding",
            "Fragmentation",
            "Application Fronting",
            "TLS fingerprint imitation",
        ],
    },

    "VLESS": {
        "category": "Proxy",
        "transports": [
            "RAW",
            "XHTTP",
            "mKCP",
            "gRPC",
            "WebSocket",
            "HTTPUpgrade",
        ],
        "security": ["TLS", "REALITY"],
        "obfuscation": [],
    },

    "VLESS": {
        "category": "Proxy",
        "transports": [],
        "encapsulation": [],
        "security": [],
        "obfuscation": [],
        "modifiers": [],
    }
}