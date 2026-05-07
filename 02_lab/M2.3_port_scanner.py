"""
Lab M2.3 — Mini Port Scanner

Obiettivo: scrivere un port scanner basico per capire come funziona nmap.

USO:
    python M2.3_port_scanner.py

ESERCIZI (in fondo al file):
    1) Scansiona un range continuo (1-1024)
    2) Aggiungi banner grabbing
    3) Confronta output con `nmap -sT 127.0.0.1`

⚠️ AVVERTENZA LEGALE ⚠️
    Scansionare host non propri (o senza autorizzazione scritta) è REATO
    in Italia (Art. 615-ter c.p.). Usa solo:
    - 127.0.0.1 (la tua macchina)
    - macchine virtuali del corso
    - target esplicitamente autorizzati (es. scanme.nmap.org per test)

    NON cambiare TARGET con IP pubblici a caso.
"""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

TARGET = "127.0.0.1"
PORTS_TO_SCAN = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445,
                 993, 995, 1433, 3306, 3389, 5432, 5900, 8080, 8443]
TIMEOUT = 1.0
MAX_WORKERS = 20

# Mappa porta → servizio (per output leggibile)
SERVICE_NAMES = {
    21: "FTP",       22: "SSH",      23: "Telnet",   25: "SMTP",
    53: "DNS",       80: "HTTP",     110: "POP3",    139: "NetBIOS",
    143: "IMAP",     443: "HTTPS",   445: "SMB",     993: "IMAPS",
    995: "POP3S",    1433: "MSSQL",  3306: "MySQL",  3389: "RDP",
    5432: "Postgres", 5900: "VNC",   8080: "HTTP-alt", 8443: "HTTPS-alt",
}


def scan_port(port: int) -> tuple[int, bool, str]:
    """
    Tenta una connessione TCP. Restituisce (porta, aperta?, motivo).

    Per capire i risultati:
    - SYN-ACK ricevuto → porta APERTA → connect() riesce
    - RST ricevuto → porta CHIUSA → ConnectionRefusedError
    - Nessuna risposta → porta FILTRATA (firewall) → timeout
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    try:
        s.connect((TARGET, port))
        return (port, True, "open")
    except ConnectionRefusedError:
        return (port, False, "closed (RST)")
    except socket.timeout:
        return (port, False, "filtered (no response)")
    except OSError as e:
        return (port, False, f"error ({e.__class__.__name__})")
    finally:
        s.close()


def main() -> None:
    print(f"[*] Scansione di {TARGET}")
    print(f"[*] Porte: {len(PORTS_TO_SCAN)}, timeout: {TIMEOUT}s, "
          f"thread: {MAX_WORKERS}\n")

    open_ports = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(scan_port, p): p for p in PORTS_TO_SCAN}
        for fut in as_completed(futures):
            port, is_open, reason = fut.result()
            service = SERVICE_NAMES.get(port, "?")
            status = "APERTA" if is_open else reason
            symbol = "[+]" if is_open else "[ ]"
            print(f"  {symbol} Porta {port:5d} ({service:10s}) : {status}")
            if is_open:
                open_ports.append(port)

    print(f"\n[+] Scansione completa. Porte aperte: {len(open_ports)}")
    if open_ports:
        print(f"[+] Lista: {sorted(open_ports)}")


if __name__ == "__main__":
    main()


# =====================================================================
# ESERCIZI
# =====================================================================
#
# ESERCIZIO 1 — Range continuo (10 min)
#   Sostituisci PORTS_TO_SCAN con `list(range(1, 1024))`.
#   Aumenta MAX_WORKERS a 100 (le porte sono molte).
#   Cosa cambia in tempo di esecuzione?
#
# ESERCIZIO 2 — Banner grabbing (15 min)
#   Dopo s.connect(), aggiungi:
#       s.sendall(b"\r\n\r\n")
#       banner = s.recv(1024)
#       print(f"  Banner: {banner.decode(errors='replace').strip()}")
#   Su porta 22 (SSH) vedrai "SSH-2.0-OpenSSH_X.Y"
#   Questo è fingerprinting: identifica la versione del servizio.
#   Perché è importante per la sicurezza?
#       Risposta: se un servizio espone la versione e la versione ha CVE
#       note, l'attaccante sa subito come bucarlo. Difesa: nascondere/modificare
#       i banner.
#
# ESERCIZIO 3 — Confronto con nmap
#   Installa nmap (su Windows: `choco install nmap`, su Linux: `sudo apt install nmap`)
#   Esegui: `nmap -sT -p 1-1024 127.0.0.1`
#   Confronta i risultati. nmap trova le stesse porte? Più? Meno?
#   Perché?
