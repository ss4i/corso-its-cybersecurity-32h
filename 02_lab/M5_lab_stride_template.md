# Lab M5 — STRIDE su BancaPiccola — Template di lavoro

**Gruppo:** ___________________________________
**Componenti:** ________________________________
**Data:** _____________________________________

---

## Fase 1 — Data Flow Diagram (15 min)

Disegna sotto il DFD del sistema BancaPiccola. Usa i 4 simboli standard:

- **Rettangolo** = entità esterna (utente, sistema esterno)
- **Cerchio** = processo (codice in esecuzione)
- **Due linee parallele** = datastore (DB, file, cache)
- **Freccia** = flusso di dati
- **Linea tratteggiata** = trust boundary

### Sistema sotto analisi

BancaPiccola, versione semplificata:

- **Frontend**: pagine HTML rese da Flask (template Jinja2)
- **Backend**: Flask, Python 3.12, server in cloud
- **DB**: SQLite, file `bancapiccola.db`
- **Funzionalità coperte**:
  - Login utente (email + password)
  - Dashboard con saldo conto
  - Lista fatture (`GET /fatture`)
  - Dettaglio fattura (`GET /fattura/<id>`)
  - Bonifico (`POST /bonifico`)
  - Upload allegato (`POST /upload`)
  - Download allegato (`GET /download?file=<nome>`)
  - Sessione persistente via cookie

### Disegno DFD

```
[Spazio per disegno]




















```

**Trust boundary identificati**:
1. _________________________________________
2. _________________________________________
3. _________________________________________

---

## Fase 2 — Tabella STRIDE (25 min)

Compila almeno **15 righe**. Per ogni elemento del DFD, almeno 2 minacce STRIDE.

| # | Elemento | Minaccia | Descrizione | Difesa |
|---|----------|----------|-------------|--------|
| 1 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 2 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 3 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 4 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 5 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 6 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 7 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 8 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 9 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 10 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 11 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 12 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 13 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 14 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |
| 15 | _______ | S/T/R/I/D/E | _________________________ | _________________________ |

---

## Fase 3 — Priorità (5 min)

Valuta ogni minaccia come **Probabilità × Impatto** (scala 1=basso, 5=alto).

Le **TOP 3** (più rischiose) da risolvere subito:

| Top | # tabella | Minaccia | Probabilità | Impatto | Rischio |
|-----|-----------|----------|-------------|---------|---------|
| 🥇 | __ | _________ | _ | _ | _ |
| 🥈 | __ | _________ | _ | _ | _ |
| 🥉 | __ | _________ | _ | _ | _ |

---

## Fase 4 — Riflessione finale (5 min)

**Una minaccia "sorprendente"** che il vostro gruppo non avrebbe identificato senza usare STRIDE in modo strutturato:

___________________________________________________

___________________________________________________

___________________________________________________

**Una difesa che richiede un cambiamento architetturale** (non solo "una riga di codice"):

___________________________________________________

___________________________________________________

___________________________________________________

---

## Suggerimenti per il docente (NON distribuire ai gruppi prima)

Esempi di minacce comuni che dovrebbero emergere:

**Spoofing**:
- Login con credenziali rubate (account takeover)
- Server fake / phishing dominio simile

**Tampering**:
- Modifica del cookie di sessione
- Modifica di parametri POST (es. `importo` nel bonifico)
- SQL Injection (caso particolare di T sul DB)

**Repudiation**:
- Utente nega di aver fatto un bonifico — manca audit trail
- Modifica/cancellazione log da parte di un attaccante

**Information Disclosure**:
- IDOR su `/fattura/<id>` (lettura fatture altrui)
- Stack trace su errore con info sensibili
- Backup DB esposto pubblicamente
- Sniffing su HTTP non cifrato (se esponi su HTTP)
- File .env esposto

**DoS**:
- Brute force login senza rate limit
- Upload di file enormi che riempie disco
- Query lente su DB

**Elevation of Privilege**:
- IDOR su PUT/DELETE per modificare/cancellare risorse altrui
- SQL Injection che permette login bypass
- Path traversal in `/download` per leggere file di sistema

Difese architetturali tipiche (non solo "una riga"):
- Migrazione SQLite → PostgreSQL con utente DB least-privilege
- Aggiunta di un WAF davanti
- Logging centralizzato e immutabile
- 2FA via TOTP
- Object Storage separato per gli upload (no filesystem locale)
- Network segmentation tra DMZ e DB
