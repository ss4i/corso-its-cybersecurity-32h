---
title: "M7 — Lab Integrato + Chiusura Corso"
subtitle: "Corso ITS Cybersecurity (32h)"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# M7 — Lab Integrato
## 2 ore — verifica trasversale applicata

## Dove sei arrivato

In 30 ore hai imparato:

- M1: CIA, principi, casi reali
- M2: rete, ISO/OSI, Wireshark, Python
- M3: HTTP, header sicurezza, cookie
- M4: GDPR, NIS 2, CRA
- M5: STRIDE, Privacy by Design
- M6: 5 vuln + supply chain + path traversal

## Cosa farai oggi

> Sei un junior security analyst.
> BancaPiccola ti chiede una **review** prima del lancio.
> Trova vulnerabilità, dimostrale, proponi fix.
> 75 minuti, report finale.

## Regole — permesso

✅ Leggere il codice sorgente
✅ DevTools, curl, requests, sqlite3
✅ Lavorare a coppie
✅ 1 hint gratis (il 2° costa -5%)
✅ Consultare le tue dispense

## Regole — non permesso

🚫 Aprire BancaPiccola-secure
🚫 Cercare su Google "BancaPiccola vuln"
🚫 Soluzioni da ChatGPT
🚫 Copiare report

## Output richiesto

File `cognome_M7_report.md`:
- Almeno **3 vulnerabilità**
- Per ognuna: severity, PoC, fix
- Categoria OWASP
- Norma violata (GDPR)

## Tempistica

| Tempo | Attività |
|-------|----------|
| 0:00 - 0:15 | Briefing |
| 0:15 - 1:30 | Lavoro (75 min) |
| 1:30 - 1:50 | Discussione collettiva |
| 1:50 - 2:00 | Chiusura corso |

## Cheat-sheet — dove cercare

| Vuln | Dove |
|------|------|
| SQLi | Form login, ricerca |
| IDOR | URL con ID (`/fattura/42`) |
| XSS | Campi rivisualizzati (commenti) |
| Crypto | Apri DB con DB Browser |
| Path Traversal | `?file=...` |

## Cheat-sheet — payload base

```
SQLi:    ' OR '1'='1     ' OR 1=1 --
XSS:     <script>alert(1)</script>
Path:    ../etc/passwd   ../app.py
```

## Bonus da cercare

- Cookie senza HttpOnly/Secure/SameSite
- Header sicurezza mancanti
- Stack trace su errore
- CVE in `requirements.txt`
- API espone campi sensibili (password_hash)

## Severity rapida

| Livello | Quando |
|---------|--------|
| Critical (9-10) | Compromissione totale, no auth |
| High (7-8.9) | Dati altrui, privesc |
| Medium (4-6.9) | Info disclosure, attacco con interazione |
| Low (0.1-3.9) | Config subottimale |

## Template del report

```markdown
### F-XX — Titolo
- Severity: ...
- CVSS stima: ...
- Localizzazione: file:riga
- OWASP: A01/A02/A03...
- CWE: ...
- GDPR: Art. ...

Descrizione: 2-3 paragrafi
PoC: comando o screenshot
Impatto: cosa succede
Fix: codice corretto
```

## Griglia di valutazione

| Voce | Peso |
|------|------|
| Numero vuln (≥3) | 20 |
| Correttezza PoC | 30 |
| Qualità fix | 30 |
| Severity giustificata | 10 |
| OWASP/GDPR | 10 |

> **Soglia 60/100**.
> Lab vale 20% del voto finale.

## Indicatori di eccellenza

- 5+ vuln (incluse 1-2 bonus)
- Vector string CVSS plausibile
- Fix architetturali, non solo patch
- Sezione compliance check
- Executive summary chiaro

## Indicatori di problemi

- "Stesse cose" come 3 vuln diverse
- Fix con `eval`, `|safe`, anti-pattern
- Severity Critical su un cookie
- Confonde MD5 e bcrypt
- Confonde 401/403

## Discussione collettiva

Ognuno presenta in 2 min:
- 1 vulnerabilità trovata
- Severity con motivazione
- Il fix proposto

Il docente:
- Confronta con BancaPiccola-secure
- Mostra pattern ricorrenti
- Risponde alle domande

# Chiusura corso

## Cosa hai imparato (concretamente)

✅ Riconoscere e classificare minacce
✅ Capire come funziona la rete
✅ Leggere richieste HTTP, header sicurezza
✅ Sapere quali norme regolano il tuo lavoro
✅ Applicare STRIDE e Privacy by Design
✅ Riconoscere e correggere 5 vulnerabilità web
✅ Usare Wireshark, DevTools, pip-audit
✅ Scrivere script Python di scanning/sniffing
✅ Fare mini security review con report

## Sei al punto di partenza

> **Non** sei un pentester
> **Non** sei un esperto di crypto
> **Sei** uno sviluppatore che vede la sicurezza

Le fondamenta sono solide.

## I 3 takeaway tra 5 anni

1. **Sicurezza si progetta** dall'inizio (Security & Privacy by Design)
2. **Difese stratificate** sempre (mai una sola)
3. **Mentalità avversaria** (cosa fa che non dovrebbe?)

## Risorse per crescere — gratuite

- **PortSwigger Web Security Academy** (gold standard)
- **TryHackMe** (rooms beginner)
- **HackTheBox starting point**
- **OverTheWire Bandit** (linux + sec)
- **OWASP** (cheat sheets)

## Certificazioni "entry"

- **CompTIA Security+** (vendor-neutral)
- **eJPT** (eLearnSecurity, hands-on)
- **PortSwigger BSCP** (Burp/AppSec)

## Da studiare al II anno ITS

- Penetration testing (Kali, Metasploit, Burp)
- Crittografia avanzata
- Cloud security (AWS/Azure/GCP)
- Container security (Docker, K8s)
- DevSecOps
- Forensics e IR

## Il messaggio finale

> "Sappiamo abbastanza per essere pericolosi"
>
> Non maestri. Ma abbastanza per **vedere** quando qualcosa non va, e per **chiedere le domande giuste**.

## In azienda

Sarete junior. Probabilmente nessuno vi chiederà esplicitamente "fate sicurezza".

Sarà il **vostro lavoro** dirla:
- Vedete una query concatenata? Alzate la mano.
- Vedete password in MD5? Alzate la mano.
- Vedete endpoint senza authz? Alzate la mano.

## Buona strada

Grazie per essere arrivati fino qui.

**Domande?**

> Per dubbi, errori in queste dispense, suggerimenti:
> parliamone alla prossima lezione.
