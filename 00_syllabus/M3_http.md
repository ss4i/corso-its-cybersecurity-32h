# M3 — Protocollo HTTP (4h)

## Obiettivo

Al termine del modulo il discente sa:

1. Spiegare il modello **richiesta/risposta** di HTTP e come si differenzia da altri protocolli.
2. Leggere e scrivere un **URL** identificandone tutte le componenti (schema, host, porta, path, query, fragment).
3. Usare correttamente i **metodi** GET, POST, PUT, PATCH, DELETE.
4. Riconoscere gli **status code** principali (2xx/3xx/4xx/5xx) e capire perché 401 ≠ 403, 404 ≠ 410, ecc.
5. Leggere gli **header HTTP** importanti, in particolare quelli **di sicurezza**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy.
6. Capire il **modello cookie/sessione** e perché HTTP è "stateless".
7. Distinguere **HTTP da HTTPS** e capire cosa fa TLS sotto.
8. Usare **DevTools** del browser, **curl** e **requests** Python per ispezionare e produrre richieste.

## Materiale di riferimento

- `Dispensa_HTTP_ITS_v2_Prodigi.docx` (riusato e adattato — è già didattica e ITS-friendly)
- `dispensa-sviluppo-sicuro-software.docx` → **Capitolo 3.1-3.8** (HTTP nel contesto delle web app)
- Materiale di approfondimento sicurezza: capitolo dedicato in `01_materiali/M3_http_sicurezza.md` (sezione "Header di sicurezza" estesa)

## Articolazione oraria

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:15 | **3.1 Cos'è HTTP** — modello client/server, stateless, plain text, evoluzione (HTTP/1.0 → HTTP/3). | Frontale |
| 0:15 – 0:35 | **3.2 URL: anatomia** — `https://user:pwd@host:port/path?query#fragment`. Quando si usa cosa. | Frontale + lavagna |
| 0:35 – 1:00 | **3.3 Metodi HTTP** — GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS. **Idempotenza** (e perché conta per la sicurezza: replay safety). | Frontale |
| 1:00 – 1:30 | **Lab M3.1 — DevTools Discovery** (30 min) — apri DevTools → Network, naviga su un sito, identifica tipi richieste, headers, body. | **Lab guidato** |
| 1:30 – 1:45 | **PAUSA** | |
| 1:45 – 2:15 | **3.4 Status code** — 2xx successo, 3xx redirect, 4xx errore client, 5xx errore server. Casi sottili: 401 vs 403, 404 vs 410, 429 (rate limit). | Frontale |
| 2:15 – 2:35 | **3.5 Header HTTP — overview** — Headers di richiesta vs risposta. `Content-Type`, `Authorization`, `Cookie`, `User-Agent`, `Host`. | Frontale |
| 2:35 – 3:15 | **3.6 Header di sicurezza** ⭐ (cuore del modulo) — CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, Set-Cookie con `Secure`/`HttpOnly`/`SameSite`. Per ognuno: cosa difende, esempio. | Frontale + esempi |
| 3:15 – 3:35 | **3.7 Cookie e sessioni** — come HTTP "ricorda". Session ID, fixation, hijacking. Anteprima difese (cookies sicuri). | Frontale |
| 3:35 – 3:55 | **Lab M3.2 — curl + requests Python** (20 min) — Replica le stesse richieste viste in DevTools, prima con `curl`, poi con `requests`. Estrae headers di sicurezza da 3 siti famosi. | **Lab guidato** |
| 3:55 – 4:00 | **3.8 HTTPS** in 5 minuti — TLS handshake, certificati, perché HTTPS ovunque. Approfondimento rimandato a M6.4 (cifratura). | Frontale |

## Lab del modulo (2h totali)

### Lab M3.1 — DevTools Discovery (30 min)

**Setup**: Chrome/Edge/Firefox aperto, DevTools attivati (F12) → tab Network.

**Consegna**:

1. Apri `https://example.com`. Quante richieste vengono fatte?
2. Apri `https://www.youtube.com`. Quante? Perché così tante?
3. Identifica una richiesta che non sia una pagina (es. font, immagine, JSON API). Apri "Headers" → analizza Request e Response.
4. Trova un cookie `Set-Cookie` con `HttpOnly` e uno senza. Spiega la differenza.

**Output**: 1 pagina con screenshot annotati (consegna individuale).

### Lab M3.2 — curl & requests (20 min)

**Setup**: terminale con `curl` installato, Python con `requests` (`pip install requests`).

**Consegna** (`02_lab/M3.2_http_client.py`):

```python
import requests

# 1) GET semplice
r = requests.get("https://httpbin.org/get")
print(r.status_code, r.json())

# 2) Headers di sicurezza di 3 siti famosi
for site in ["https://github.com", "https://google.com", "https://example.com"]:
    r = requests.get(site)
    print(f"\n=== {site} ===")
    for h in ["Strict-Transport-Security", "Content-Security-Policy",
              "X-Frame-Options", "X-Content-Type-Options"]:
        print(f"  {h}: {r.headers.get(h, 'MANCANTE')}")
```

**Discussione**: chi ha più header di sicurezza? Chi ne ha meno? Perché?

### Lab M3.3 — opzionale, fine giornata: IDOR esplorativo

Dalla `Dispensa_HTTP_ITS_v2`, capitolo 9 lab pratico — anteprima del Modulo M6 (Broken Access Control). Si fa solo se avanza tempo o come esercizio per casa.

## Verifica

Le domande di M3 entrano in **V1 (verifica intermedia post M3)**.

Esempi:

- Quale status code restituiresti se l'utente non è autenticato? E se è autenticato ma non autorizzato?
- Cosa fa `HSTS` e perché protegge contro un downgrade attack?
- Differenza tra cookie con `SameSite=Strict`, `Lax`, `None`. Quando si usa cosa?
- Perché non si dovrebbero mettere dati sensibili nella query string di una GET?

## Errori da evitare in classe

- **Non liquidare in 30 secondi gli header di sicurezza** — sono tra le difese più efficaci e meno costose. Vale la pena dedicarci 40 minuti.
- **Non insegnare HTTPS senza prima aver fatto vedere HTTP in chiaro** in Wireshark (M2). Il "perché" si capisce solo dopo aver visto cosa si vede senza TLS.
- **Non confondere autenticazione e autorizzazione** già qui — è il tema centrale di M6.2 (IDOR).
