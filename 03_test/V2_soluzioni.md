# Verifica V2 — SOLUZIONI

**Punteggio totale:** 100
**Soglia di sufficienza:** 60

---

## Sezione A — Scelta multipla (15 × 2 = 30)

| # | Risposta | Note |
|---|----------|------|
| A1 | **b** | Art. 25 GDPR — Privacy by design and by default |
| A2 | **c** | 72 ore (Art. 33 GDPR) |
| A3 | **b** | 20M€ o 4% fatturato (il maggiore) |
| A4 | **c** | Settori essenziali e importanti (allegati I e II) |
| A5 | **b** | Reg. 2024/2847, in vigore dicembre 2027 |
| A6 | **b** | Threat modeling |
| A7 | **b** | Tampering (manomissione) |
| A8 | **c** | Elevation of Privilege |
| A9 | **b** | Spostare la sicurezza presto nel ciclo |
| A10 | **c** | Due linee parallele = datastore |
| A11 | **b** | Linea che separa zone con livelli di fiducia diversi |
| A12 | **c** | "Encryption Everywhere" non è uno dei 7. I 7 sono: Proactive, Privacy as Default, Embedded into Design, Full Functionality, End-to-End Security, Visibility/Transparency, Respect for User Privacy |
| A13 | **b** | Pseudonimizzato = ancora dato personale, GDPR si applica |
| A14 | **c** | Anonimizzazione = irreversibile anche con dati esterni |
| A15 | **c** | Rischio elevato (Art. 35 GDPR + lista Garante) |

---

## Sezione B — Risposta breve (5 × 4 = 20)

### B1. Pseudonimizzazione vs Anonimizzazione

**Pseudonimizzazione**: i dati identificativi sono sostituiti da un identificatore artificiale (pseudonimo), ma **esiste una mappa** di reidentificazione (separata). È **reversibile** tramite la mappa. **GDPR si applica ancora**.

**Anonimizzazione**: il legame con l'individuo è **irreversibile**, anche incrociando con dati esterni. **GDPR non si applica**.

**Quale richiede il rispetto del GDPR**: la **pseudonimizzazione** (sì, sempre).

> 2 pt definizioni + 2 pt risposta GDPR.

### B2. App di salute — 3 misure tecniche

Tre tra (con una breve giustificazione):

1. **Cifratura** dei dati a riposo (DB cifrato) e in transito (TLS 1.2+).
2. **Pseudonimizzazione** dei record (separare identità anagrafica e dati sanitari).
3. **Controllo accessi** rigoroso (least privilege, MFA).
4. **Logging audit** delle accessi ai dati sensibili.
5. **Retention policy** automatica (cancellazione dopo periodo previsto).
6. **Backup cifrato** e separato.

> 4 pt: 1.3 per ogni misura corretta + bonus se cita Art. 32 testualmente.

### B3. Spoofing vs Tampering

- **Spoofing** = fingere un'identità falsa. Esempio in BancaPiccola: login con password rubata di un altro utente, oppure server fake con dominio simile per phishing.
- **Tampering** = modificare dati/codice. Esempio in BancaPiccola: modifica dell'importo nel POST `/bonifico` (es. da 100€ a 10000€), oppure modifica del cookie di sessione per impersonare un altro user_id.

> 1 pt definizione Spoofing + 1 pt esempio + 1 pt definizione Tampering + 1 pt esempio.

### B4. 4 domande di Shostack

1. **Cosa stiamo costruendo?** (Disegna il sistema — DFD)
2. **Cosa può andare storto?** (Applica un framework, es. STRIDE)
3. **Cosa facciamo a riguardo?** (Mitigare/accettare/trasferire/eliminare)
4. **Abbiamo fatto un buon lavoro?** (Review collettiva, aggiornamento)

> 1 pt per domanda.

### B5. CIA per BancaPiccola

| Azione | C / I / A |
|--------|-----------|
| Bonifico effettuato dall'utente | **I** (deve restare integro: importo, destinatario) |
| Lista password dei clienti | **C** (riservatezza assoluta) |
| Accesso alla pagina di login durante un picco di traffico | **A** (deve essere disponibile) |
| Modifica del saldo del conto via SQL Injection | **I** (modifica non autorizzata) — accettabile anche **C** se lettura dati |

> 1 pt per ogni risposta corretta.

---

## Sezione C — STRIDE (30)

### Esempio di soluzione (DFD)

```
[Cliente]──HTTP──┬──────────────TLS────────────────►[Frontend Flask]──┐
                 │                                                     │
        ═══ Boundary: Internet ════════════════════════════════════════│
                                                                       │
                                                  ┌────────────────────┘
                                                  ▼
                                            [Auth/Auth Service]
                                                  │
                                                  ▼
                                            [Order Service]
                                                  │
                              ═══════ Boundary: server ↔ DB ═══════════
                                                  │
                                                  ▼
                                          [PostgreSQL DB]
                                                  ▲
                                                  │
                                            [Email/Stripe API]──Internet
                              ═══════ Boundary: server ↔ esterno ══════
```

### Esempio di tabella STRIDE (9 minacce)

| # | Elemento | STRIDE | Descrizione | Difesa |
|---|----------|--------|-------------|--------|
| 1 | Login (processo) | S | Account takeover via password rubata | MFA + password policy |
| 2 | Order (processo) | E | IDOR in `/ordine/<id>` | Ownership check server-side |
| 3 | Order (processo) | E | SQLi in ricerca prodotti | Query parametrizzate |
| 4 | DB | I | Backup non cifrato esposto | Cifrare backup + accesso ristretto |
| 5 | DB | T | Modifica saldo via SQLi | Query parametrizzate + least priv DB |
| 6 | Flusso server↔Stripe | T | MITM su API Stripe | TLS + verify certificate + webhook signature |
| 7 | Auth | R | Utente nega ordine | Audit log immutabile + firma digitale ordine |
| 8 | Login (processo) | D | Brute force | Rate limit + CAPTCHA + account lockout |
| 9 | Frontend | I | Stack trace su errore con SQL | Error handler generico + logging interno |

### Minaccia più grave — esempio risposta

> "La SQL Injection nel motore di ricerca (riga 3) è la più grave perché:
> - Probabilità: alta (campi di ricerca sono il primo bersaglio).
> - Impatto: critico (estrazione DB completo, inclusi dati clienti, password hash, dati di pagamento se non isolati).
> - Effetto a cascata: trigger di obblighi GDPR/NIS2."

> Punteggio: 8 pt DFD + 18 pt tabella (2 pt per minaccia, max 9) + 4 pt motivazione.

---

## Sezione D — DPIA (20)

### D1. DPIA obbligatoria? (5 pt)

**Sì, obbligatoria** perché:
- Trattamento di **dati biometrici** (categoria particolare, Art. 9 GDPR).
- Sorveglianza sistematica di soggetti vulnerabili (studenti, spesso minorenni).
- Profilazione automatica.
- Lista nera del Garante Italiano cita esplicitamente sistemi di riconoscimento facciale.

> 2 pt risposta corretta + 3 pt motivazione completa.

### D2. Rischi per gli interessati (5 pt)

Almeno 3 tra:
- **Furto di dati biometrici** (irreversibili — non puoi cambiare il volto come una password).
- **Discriminazione** se il sistema ha bias (etnia, genere, età).
- **Profilazione comportamentale** non consentita (orari, ritardi).
- **Function creep**: i dati raccolti per presenze finiscono per altri usi.
- **Effetto chilling**: studenti modificano comportamento sapendo di essere sorvegliati.
- **Data breach**: se il sistema è bucato, leak di template biometrici.
- **Mancanza di consenso libero** (rapporto asimmetrico scuola-studente).

> 1.7 pt per rischio (max 5).

### D3. Alternativa con data minimization (5 pt)

Esempio di risposta corretta:

> "Il riconoscimento facciale **non è necessario**: registrare la presenza si può fare con metodi meno invasivi:
> 1. **Badge RFID/NFC** già usato per accesso fisico — basta un lettore ai tornelli.
> 2. **App con QR code** che lo studente scansiona all'ingresso (autenticazione a 2 fattori se serve).
> 3. **Appello manuale digitalizzato** dal docente.
>
> Tutti questi raggiungono lo stesso obiettivo (presenze certe) senza dati biometrici. La proporzionalità (Art. 5 GDPR) richiede il **mezzo meno invasivo**: il riconoscimento facciale è sproporzionato per il fine."

> 5 pt per soluzione corretta + motivazione + riferimento a proporzionalità.

### D4. Misure (5 pt)

**Tecniche** (esempi):
- Cifratura template biometrici a riposo + canale TLS.
- Conservazione **del solo template**, non dell'immagine; eliminazione foto immediatamente dopo l'estrazione del template.
- Riduzione retention da 30 giorni a 0 (basta la presenza registrata, non la foto).

**Organizzative**:
- Informativa specifica e consenso esplicito (con possibilità di alternativa, vedi punto 3).
- Nomina DPO + audit periodico.
- Formazione del personale.
- Procedura per esercizio diritti GDPR (Art. 15-22).

> 1.25 pt per misura (max 5).

---

## Griglia di valutazione

| Voto | Range punti |
|------|-------------|
| Eccellente | 90-100 |
| Buono | 75-89 |
| Sufficiente | 60-74 |
| Insufficiente | < 60 |
