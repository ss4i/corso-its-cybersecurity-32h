---
title: "M2 — Networking & ISO/OSI"
subtitle: "Corso ITS Cybersecurity (32h)"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# M2 — Networking & ISO/OSI
## 6 ore — 3h teoria + 3h lab

## Obiettivi

- Stack ISO/OSI vs TCP/IP
- Vulnerabilità per ogni livello
- **Wireshark** in pratica
- Python: socket, port scanner, scapy
- Avviso legale: sniffing su reti non proprie = reato

## L'analogia postale

- Tu scrivi la **lettera** (= app)
- La metti in **busta** con mittente/destinatario (= IP)
- Le poste fanno **smistamento** (= router)
- Camion / aereo / postino (= livelli sotto)

Ogni livello fa il suo pezzo. Non sa cosa fanno gli altri.

## ISO/OSI — i 7 livelli

| # | Nome | Esempi |
|---|------|--------|
| 7 | Application | HTTP, FTP, DNS |
| 6 | Presentation | TLS, JSON, ASCII |
| 5 | Session | RPC |
| 4 | Transport | TCP, UDP |
| 3 | Network | IP, ICMP, ARP |
| 2 | Data Link | Ethernet, Wi-Fi |
| 1 | Physical | Cavi, fibra, radio |

## TCP/IP — modello pratico (4 livelli)

| TCP/IP | OSI |
|--------|-----|
| Application | 5+6+7 |
| Transport | 4 |
| Internet | 3 |
| Network Access | 1+2 |

> ISO/OSI = mappa concettuale. TCP/IP = realtà.

## Incapsulamento

```
HTTP request           ← Livello 7
  ↓
TLS encrypted          ← Livello 6
  ↓
TCP segment (port 443) ← Livello 4
  ↓
IP packet (dst IP)     ← Livello 3
  ↓
Ethernet frame (MAC)   ← Livello 2
  ↓
Bit elettrici          ← Livello 1
```

Ogni livello aggiunge un header.

## Livello 1-2 — Fisico e Data Link

- **MAC address**: 48 bit, fisso, per scheda di rete
- **Frame Ethernet**: busta L2 con MAC src/dst + payload
- **Switch**: inoltra per MAC
- **Vulnerabilità**: MAC spoofing, MAC flooding, VLAN hopping
- **Difesa**: port security, DAI, 802.1X

## ARP — IP → MAC

- Hai l'IP, ti serve il MAC
- ARP request in **broadcast**: "chi ha 192.168.1.10?"
- Solo lui risponde con il proprio MAC
- Cache locale: `arp -a`

## ARP Spoofing (= MITM)

- ARP **non ha autenticazione**
- Attaccante invia ARP non richiesti dicendo "il gateway sono io"
- Vittima ci crede → traffico passa dall'attaccante
- **Tool**: ettercap, bettercap

> Difesa: ARP statico, DAI, **HTTPS ovunque**

## Livello 3 — IP, ICMP, routing

- **IPv4**: 32 bit (~4 miliardi)
- **IPv6**: 128 bit (per il futuro)
- IP privati: 10.x, 172.16-31.x, 192.168.x
- **NAT**: traduce privato↔pubblico

## Vulnerabilità L3

- **IP spoofing**: mittente falsificato
- **ICMP flood / Ping of Death**
- **Smurf attack**: ping con broadcast + IP vittima spoofato
- **Tear drop**: pacchetti frammentati malformati

> Difese: firewall, reverse path filtering, rate limit

## Livello 4 — Trasporto

| | TCP | UDP |
|---|-----|-----|
| Connessione | Sì (handshake) | No |
| Affidabilità | Sì | No |
| Ordine | Sì | No |
| Velocità | Lenta | Veloce |
| Casi d'uso | HTTP, SSH, FTP | DNS, VoIP, gaming |

## Three-way handshake TCP

```
Client                       Server
  ── SYN ───►
              ◄── SYN-ACK ──
  ── ACK ───►
   ═══ Connessione stabilita ═══
```

3 messaggi e si parte. **Lo vedrete in Wireshark**.

## Le porte

- 0–1023: well-known (22 SSH, 80 HTTP, 443 HTTPS)
- 1024–49151: registered
- 49152–65535: dynamic (client effemere)

> Fingerprinting: porta aperta + banner = versione software

## Vulnerabilità L4 (TCP)

- **Port scanning** (nmap, base ricognizione)
- **SYN flood** (DoS — il server riserva risorse)
- **TCP hijacking** (raro grazie a seq randomizzati)
- **TCP reset attacks**

## Vulnerabilità L4 (UDP)

- **UDP flood** (no handshake = facile DoS)
- **DNS amplification** (50-100x amplification)
- **NTP amplification**

## Livelli 5-7 — sopra il trasporto

- **DNS** (UDP/53): traduce nomi → IP
- **TLS**: cifra dati di livello applicativo
- **HTTP**: cuore del web (M3)
- **SMTP/IMAP**: email
- **SSH**: shell remota cifrata

## Vulnerabilità DNS

- **DNS spoofing / cache poisoning**
- **DNS hijacking**
- **DNS tunneling** (canale C2 furtivo)

> Difesa: DNSSEC, DoT/DoH

## Vulnerabilità TLS

- **Heartbleed (2014)** — letta memoria server
- **POODLE, BEAST, CRIME**
- **Downgrade attacks** → difesa: HSTS
- **Certificati invalidi** se accettati = MITM

## Difese stratificate

| Livello | Vulnerabilità | Difesa |
|---------|---------------|--------|
| 7 | XSS, SQLi, IDOR | Codice sicuro (M6) |
| 6 | TLS downgrade | HSTS |
| 5 | Session hijack | Cookie sicuri |
| 4 | SYN flood | Rate limit |
| 3 | IP spoofing | RPF |
| 2 | ARP spoof | DAI |
| 1 | Wiretapping | Sicurezza fisica |

## ⚠️ Avviso legale

> **Sniffing/scanning su reti non proprie = REATO**
> - Art. 615-ter c.p. (accesso abusivo)
> - Art. 617-quater c.p. (intercettazione illecita)

Lab solo su:
- 127.0.0.1
- VM del corso
- Target esplicitamente autorizzati

## Lab M2.1 — Wireshark Discovery (45 min)

- Cattura HTTP in chiaro su example.com
- Filtra `http` → vedi GET/Response
- Cattura HTTPS → vedi solo TLS handshake (cifrato)
- Filtra `tcp.flags.syn==1` → vedi 3-way handshake
- Filtra `dns` → vedi risoluzione

## Lab M2.2 — Socket TCP Python

```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("example.com", 80))
s.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
print(s.recv(4096))
```

In parallelo: Wireshark conferma che è la **stessa cosa** del browser.

## Lab M2.3 — Port Scanner

```python
for port in [21, 22, 80, 443, 3306]:
    s = socket.socket(...)
    s.settimeout(1)
    try:
        s.connect((TARGET, port))
        print(f"{port} aperta")
    except: pass
```

Confronta con `nmap -sT 127.0.0.1`.

## Lab M2.4 — Scapy Sniff

```python
from scapy.all import sniff, IP, TCP

def cb(p):
    if IP in p:
        print(f"{p[IP].src} -> {p[IP].dst}")

sniff(prn=cb, count=30, store=False)
```

Richiede privilegi root/admin.

## Cosa portarsi a casa

- ✅ Pila ISO/OSI a 7 livelli
- ✅ Vulnerabilità per livello
- ✅ TCP vs UDP
- ✅ Wireshark per leggere il traffico
- ✅ Python per scriverlo

> La sicurezza è layered: defense in depth.

## Prossimo modulo

**M3 — Protocollo HTTP (4h)**

Adesso che sai come arrivano i bit, vediamo cosa c'è dentro le richieste HTTP.
