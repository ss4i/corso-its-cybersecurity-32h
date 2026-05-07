"""
Lab M2.2 — Client TCP con socket Python

Obiettivo: scrivere a mano una richiesta HTTP usando i socket TCP del livello 4
e confrontare con cattura Wireshark in parallelo.

USO:
    python M2.2_socket_tcp.py

NOTA LEGALE:
    Questo script si collega solo a example.com (host pubblico esplicitamente
    autorizzato per i test). NON modificare HOST con IP a caso.
"""

import socket

HOST = "example.com"
PORT = 80
TIMEOUT = 5.0


def main() -> None:
    # Step 1: crea socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)

    try:
        # Step 2: connetti — questo scatena il three-way handshake!
        # (osservalo in Wireshark con filtro `tcp.flags.syn == 1`)
        s.connect((HOST, PORT))
        print(f"[+] Connesso a {HOST}:{PORT}")

        # Step 3: invia richiesta HTTP costruita a mano
        request = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {HOST}\r\n"
            f"User-Agent: ITS-Cybersec-Lab/1.0\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )
        s.sendall(request.encode("ascii"))
        print(f"[>] Inviata richiesta GET / di {len(request)} byte\n")

        # Step 4: leggi la risposta a chunk
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

        # Stampa la risposta (header + body)
        print("=" * 60)
        print(response.decode("utf-8", errors="replace"))
        print("=" * 60)
        print(f"\n[+] Ricevuti {len(response)} byte totali")

    except socket.timeout:
        print(f"[!] Timeout dopo {TIMEOUT}s")
    except OSError as e:
        print(f"[!] Errore di rete: {e}")
    finally:
        s.close()


if __name__ == "__main__":
    main()


# DOMANDE DI APPROFONDIMENTO:
#
# 1) Cosa cambia se rimuovi `Connection: close` dalla richiesta?
#    Risposta: il server tiene aperta la connessione (HTTP/1.1 keep-alive).
#    Il tuo loop `while True` non riceve mai chunk vuoto e vai in timeout.
#
# 2) Perché `\r\n` e non `\n`?
#    Risposta: HTTP è specificato con CRLF come line terminator.
#    Molti server tollerano `\n`, ma non è garantito.
#
# 3) Cambia HOST a "https://example.com" — funziona?
#    Risposta: NO. La porta 443 parla TLS, non HTTP plain.
#    Per HTTPS serve il modulo `ssl` di Python (esercizio extra).
