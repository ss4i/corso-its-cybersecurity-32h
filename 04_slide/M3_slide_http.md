---
title: "M3 — Protocollo HTTP"
subtitle: "Corso ITS Cybersecurity (32h)"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# M3 — Protocollo HTTP
## 4 ore — 2h teoria + 2h lab

## Obiettivi

- Modello richiesta/risposta
- URL, metodi, status code
- **Header di sicurezza** (cuore del modulo)
- Cookie sicuri (Secure, HttpOnly, SameSite)
- HTTPS/TLS in dettaglio

## HTTP in 30 secondi

- **Stateless**: ogni richiesta indipendente
- **Plain text** (in HTTP); cifrato (in HTTPS)
- Modello **request/response**
- Versioni: HTTP/1.0, 1.1, 2, 3

## URL — anatomia

```
https://user:pwd@host:port/path?query#fragment
```

| Pezzo | Esempio |
|-------|---------|
| schema | `https` |
| host | `example.com` |
| port | `:443` (default per HTTPS) |
| path | `/api/users` |
| query | `?id=42` |
| fragment | `#sezione` |

## Metodi HTTP

| Metodo | Uso | Idempotente? |
|--------|-----|--------------|
| GET | Leggi | Sì |
| POST | Crea | No |
| PUT | Sostituisci | Sì |
| PATCH | Modifica | No (in pratica) |
| DELETE | Cancella | Sì |
| HEAD | Solo header | Sì |

## Status code 4xx — sottili

- **400** — Bad Request (sintassi)
- **401** — Unauthorized = **non autenticato**
- **403** — Forbidden = autenticato ma **non autorizzato**
- **404** — Not Found
- **410** — Gone (rimosso volontariamente)
- **422** — Unprocessable Entity (semantica)
- **429** — Too Many Requests (rate limit)

## Status code 5xx

- **500** — Internal Error (NON rivelare stack trace!)
- **502** — Bad Gateway
- **503** — Service Unavailable (con `Retry-After`)
- **504** — Gateway Timeout

## I 6 header di sicurezza fondamentali

1. `Strict-Transport-Security` (HSTS)
2. `Content-Security-Policy` (CSP)
3. `X-Frame-Options`
4. `X-Content-Type-Options`
5. `Referrer-Policy`
6. `Permissions-Policy`

## HSTS

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

- Forza il browser a usare **sempre HTTPS**
- Difende da **SSL stripping**
- `preload` = nella lista hardcoded dei browser

## Content-Security-Policy

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-r4nd0m';
  frame-ancestors 'none'
```

- Limita da dove caricare risorse
- **Difesa principale contro XSS** (insieme all'escape)
- Mai `'unsafe-inline'` o `'unsafe-eval'` se evitabili

## X-Frame-Options & X-Content-Type-Options

```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
```

- `DENY` blocca clickjacking
- `nosniff` impedisce MIME sniffing del browser

## Referrer-Policy & Permissions-Policy

```
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(self)
```

- Controlla cosa va nel `Referer` cross-site
- Limita le API browser disponibili

## Cookie sicuri — i 3 attributi

```
Set-Cookie: session=abc123;
            Secure;
            HttpOnly;
            SameSite=Lax
```

- **Secure**: solo su HTTPS
- **HttpOnly**: JS non può leggerlo (anti-XSS)
- **SameSite**: anti-CSRF

## SameSite a fondo

- **Strict**: mai cross-site (UX restrittiva)
- **Lax**: solo top-level cross-site (default moderno)
- **None**: sempre (richiede `Secure`)

## Flask configurazione cookie

```python
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=3600,
)
```

## HTTPS — cosa fa TLS

1. **Cifratura** (i messaggi non sono leggibili)
2. **Autenticazione** (verifica certificato server)
3. **Integrità** (modifica = rilevabile)

## Versioni TLS

| Versione | Stato |
|----------|-------|
| SSL 1/2/3 | ❌ MORTO |
| TLS 1.0/1.1 | ❌ Deprecato 2020 |
| TLS 1.2 | ✅ OK (standard) |
| TLS 1.3 | ✅ Migliore |

## TLS handshake (1.2 semplificato)

```
Client → Server: ClientHello (versioni, cipher)
Server → Client: ServerHello + Certificate + KeyExchange
Client → Server: KeyExchange + ChangeCipherSpec + Finished
Server → Client: ChangeCipherSpec + Finished
═══ Canale cifrato ═══
```

## Errori TLS comuni

| Sintomo | Causa |
|---------|-------|
| Cert authority invalid | Self-signed |
| Cert expired | Scaduto, manca rinnovo |
| Name mismatch | Cert non copre quel dominio |
| Mixed content | HTTPS che carica HTTP |

> Test: SSL Labs (ssllabs.com/ssltest)

## Vulnerabilità protocollo (cenni)

- **HTTP request smuggling**: front/back interpretano diversamente
- **Response splitting**: `\r\n` injection in header
- **Slowloris**: connessioni lentissime → DoS

## Lab M3.1 — DevTools Discovery

- Apri DevTools (F12) → Network
- Visita 3 siti (github, google, esempio italiano)
- Annota: # richieste, status code, 3 header, cookie

## Lab M3.2 — `requests` Python

```python
import requests
r = requests.get("https://github.com")
for h in ["Strict-Transport-Security",
          "Content-Security-Policy",
          "X-Frame-Options"]:
    print(h, r.headers.get(h, "MISS"))
```

Confronto: chi ne ha più? Chi ne ha meno?

## Checklist HTTP per la tua webapp

- [ ] TLS 1.2+ (idealmente 1.3)
- [ ] Cert valido, no self-signed
- [ ] HSTS, CSP, XFO, XCTO, Referrer-Policy
- [ ] Cookie Secure + HttpOnly + SameSite
- [ ] `Server` rimosso/oscurato
- [ ] Error handler 500 generico
- [ ] Rate limit + 429 + Retry-After
- [ ] No password in query string

## Verifica intermedia V1

> Alla fine di M3 — 60 minuti, 100 punti
> Copre M0-M3

Cosa entra:
- CIA, principi Secure Coding
- Stack OSI, protocolli
- HTTP, header, cookie
- Mini esercizi pratici

## Prossimo modulo

**M4 — Quadro Normativo (2h)**

Sai cosa fare tecnicamente. Ora vediamo cosa la legge **richiede**.
