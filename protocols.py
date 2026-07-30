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

Transport_protocols = [
    "TCP",
    "UDP",
    "QUIC",
    "HTTP/2",
    "HTTP/3",
    "WebSocket",
    "WebSocket Secure",
    "gRPC",
    "xHTTP",
    "KCP",
    "DomainSocket"
]

Obfuscation = [
    "TLS",
    "REALITY",
    "uTLS",
    "FakeTLS",
    "Padding",
    "Fragmentation",
    "SNI Spoofing",
    "Domain Fronting",
    "CDN masking",
    "Randomized packets",
    "XTLS",
    "Obfs4"
]

protocols_fut = {
    "VPN": {
        "OpenVPN", 
        "WireGuard", 
        "AmneziaWG", 
        "Lightway", 
        "SoftEther", 
        "IKEv2/IPSec"
#        "WARP"
        },

    "Proxy": {
        "SOCKS5",  
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
        "MTProto Proxy"},

    #"Other": {
    #    "psiphon3",
    #    "QUIC":[
    #        "Hysteria", 
    #        "Hysteria2",
    #        "TUIC",
    #    ]
    #    }

    }