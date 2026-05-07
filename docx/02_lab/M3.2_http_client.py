"""
Lab M3.2 — HTTP Client con `requests` + analisi header di sicurezza

Obiettivo:
    1) Replicare richieste viste in DevTools usando Python `requests`
    2) Analizzare gli header di sicurezza di siti famosi
    3) Capire quali siti sono "ben configurati" e quali no

USO:
    pip install requests
    python M3.2_http_client.py
"""

import requests

# Header di sicurezza che ogni sito serio dovrebbe avere
SECURITY_HEADERS = [
    "Strict-Transport-Security",        # HSTS — forza HTTPS
    "Content-Security-Policy",          # CSP — limita risorse caricabili
    "X-Frame-Options",                  # blocca clickjacking
    "X-Content-Type-Options",           # blocca MIME sniffing
    "Referrer-Policy",                  # controlla che URL sono inviati al referer
    "Permissions-Policy",               # controlla feature browser (camera, microfono)
]


def analyze_site(url: str) -> None:
    """Stampa un report sugli header di sicurezza di `url`."""
    print(f"\n=== {url} ===")
    try:
        r = requests.get(url, timeout=10, allow_redirects=True)
    except requests.RequestException as e:
        print(f"  [!] Errore: {e}")
        return

    print(f"  Status: {r.status_code}")
    print(f"  Server: {r.headers.get('Server', 'N/A')}")
    print(f"  URL finale (dopo redirect): {r.url}")
    print(f"\n  Header di sicurezza:")

    score = 0
    for h in SECURITY_HEADERS:
        value = r.headers.get(h)
        if value:
            score += 1
            # Tronca valori lunghi (CSP può essere lunga)
            shown = value if len(value) <= 60 else value[:57] + "..."
            print(f"    [✓] {h}: {shown}")
        else:
            print(f"    [✗] {h}: MANCANTE")

    print(f"\n  Punteggio: {score}/{len(SECURITY_HEADERS)}")


def main() -> None:
    print("Lab M3.2 — Analisi Header di Sicurezza")
    print("=" * 60)

    # Esempio 1: GET semplice con httpbin (utile per debug)
    print("\n[1] GET semplice a httpbin.org/get")
    r = requests.get("https://httpbin.org/get", timeout=10)
    print(f"  Status: {r.status_code}")
    print(f"  Origin (il tuo IP da httpbin): {r.json().get('origin')}")
    print(f"  User-Agent inviato: {r.json()['headers'].get('User-Agent')}")

    # Esempio 2: 4 siti reali a confronto
    print("\n[2] Confronto header di sicurezza")
    for site in [
        "https://github.com",
        "https://www.google.com",
        "https://example.com",
        "https://www.python.org",
    ]:
        analyze_site(site)

    print("\n" + "=" * 60)
    print("DOMANDA: chi ha il punteggio più alto? Perché?")
    print("DOMANDA: quale header manca a quasi tutti? Quale è il più diffuso?")


if __name__ == "__main__":
    main()


# =====================================================================
# ESERCIZI
# =====================================================================
#
# ESERCIZIO 1 — POST autenticato
#   Aggiungi una funzione che fa POST a httpbin.org/post con:
#     - body JSON: {"username": "alice", "action": "login"}
#     - header personalizzato: "X-API-Key: lab-corso-its"
#   Stampa la risposta e verifica che httpbin "ribadisca" body e headers.
#
# ESERCIZIO 2 — Cookie e sessioni
#   Usa `s = requests.Session()` invece di `requests.get()` per chiamate
#   ripetute. Visita 3 volte httpbin.org/cookies/set?name=alice e
#   stampa s.cookies dopo. Che differenza c'è rispetto a chiamate singole?
#
# ESERCIZIO 3 — User-Agent custom
#   Cambia lo User-Agent della tua sessione a "Mozilla/5.0 ..." (un browser
#   normale). Confronta cosa cambia. Alcuni siti (es. cloudflare-protected)
#   bloccano User-Agent "python-requests/X.Y" di default.
#
# ESERCIZIO 4 — HTTPS con certificato sbagliato
#   Visita https://expired.badssl.com — cosa succede?
#   Per saltare la verifica (NON FARLO MAI in produzione):
#     r = requests.get("https://expired.badssl.com", verify=False)
#   Perché disabilitare la verifica è una pessima idea?
#
# DOMANDA DI APPROFONDIMENTO:
#   Visita https://securityheaders.com e analizza un sito di tua scelta.
#   Confronta il loro punteggio con quello del tuo script.
