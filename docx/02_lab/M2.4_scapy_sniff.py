"""
Lab M2.4 — Mini Sniffer con Scapy

Obiettivo: catturare pacchetti dalla propria interfaccia di rete in Python
e capire i livelli OSI in azione.

USO:
    Linux/macOS:  sudo python M2.4_scapy_sniff.py
    Windows:      esegui PowerShell come Amministratore, poi:
                  python M2.4_scapy_sniff.py

PREREQUISITI:
    pip install scapy

⚠️ AVVERTENZA LEGALE ⚠️
    Lo sniffing di rete è REATO se fatto su reti non proprie senza
    autorizzazione (Art. 617-quater c.p. — Intercettazione illecita).

    Usa solo:
    - la tua rete domestica
    - macchine virtuali del corso
    - reti di laboratorio esplicitamente autorizzate

    NON catturare in:
    - Wi-Fi pubblici (caffè, aeroporto, biblioteca)
    - reti aziendali/scolastiche senza autorizzazione scritta
"""

from scapy.all import sniff, IP, IPv6, TCP, UDP, DNS, ICMP


def process_packet(pkt) -> None:
    """Stampa una riga sintetica per ogni pacchetto."""

    # Layer 3: IP (v4 o v6)
    if IP in pkt:
        src = pkt[IP].src
        dst = pkt[IP].dst
    elif IPv6 in pkt:
        src = pkt[IPv6].src
        dst = pkt[IPv6].dst
    else:
        return  # ignora pacchetti non-IP (es. ARP a basso livello)

    # Layer 4: TCP, UDP, ICMP
    if TCP in pkt:
        proto = "TCP"
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport
        flags = pkt[TCP].flags  # SYN, ACK, FIN, RST...
        extra = f"flags={flags}"
    elif UDP in pkt:
        proto = "UDP"
        sport = pkt[UDP].sport
        dport = pkt[UDP].dport
        extra = ""
        # Layer 7 dentro UDP: DNS?
        if DNS in pkt and pkt[DNS].qd is not None:
            extra = f"DNS query: {pkt[DNS].qd.qname.decode(errors='replace')}"
    elif ICMP in pkt:
        proto = "ICMP"
        sport = "-"
        dport = "-"
        extra = f"type={pkt[ICMP].type}"
    else:
        proto = "OTHER"
        sport = "-"
        dport = "-"
        extra = ""

    print(f"[{proto:5s}] {src}:{sport} -> {dst}:{dport}  {extra}")


def main() -> None:
    print("[*] Cattura 30 pacchetti dall'interfaccia di default")
    print("[*] Apri il browser per generare traffico\n")

    sniff(
        prn=process_packet,
        count=30,
        store=False,
        # filter="tcp port 80 or tcp port 443"  # decommentare per filtro BPF
    )

    print("\n[+] Cattura completa.")


if __name__ == "__main__":
    main()


# =====================================================================
# ESERCIZI
# =====================================================================
#
# ESERCIZIO 1 — Filtro BPF
#   Decommentare la riga `filter=...` per catturare solo HTTP/HTTPS.
#   Sintassi BPF: https://www.tcpdump.org/manpages/pcap-filter.7.html
#   Prova:
#     - "tcp port 80"
#     - "tcp port 443"
#     - "udp port 53" (solo DNS)
#     - "icmp" (solo ping)
#
# ESERCIZIO 2 — Salva in pcap
#   Modifica per salvare la cattura su file leggibile da Wireshark:
#       packets = sniff(count=30, filter="tcp port 443")
#       wrpcap("capture.pcap", packets)
#   Poi apri capture.pcap con Wireshark.
#
# ESERCIZIO 3 — Analisi DNS
#   Filtra solo DNS query (`filter="udp port 53"`) e raccogli tutti i nomi
#   risolti. Quali servizi sta contattando il tuo PC?
#   (Spoiler: ne troverai molti più di quelli che pensavi.)
#
# DOMANDE DI VERIFICA:
#
# Q1) Perché serve essere root/admin per fare sniffing?
#     Risposta: la cattura di pacchetti richiede l'apertura della scheda
#     in "promiscuous mode", privilegio che il SO riserva ad admin.
#
# Q2) Lo sniffer vede tutto il traffico della rete o solo quello del PC?
#     Risposta: dipende. Su switch moderni vedi solo il tuo (lo switch
#     instrada per MAC). Su Wi-Fi senza WPA2-Enterprise potresti vedere
#     traffico di altri se sei su stesso AP. Su rete con hub o ARP-spoofed
#     vedi più di quanto dovresti.
#
# Q3) Vedi anche il payload HTTP?
#     Risposta: solo per traffico in chiaro (HTTP, FTP, Telnet). HTTPS è
#     cifrato dopo il TLS handshake — vedi solo headers TCP/IP, non il body.
