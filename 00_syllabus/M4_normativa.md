# M4 — Quadro Normativo (2h, no lab)

## Obiettivo

Al termine del modulo il discente sa:

1. Citare le **3 norme principali** che riguardano lo sviluppatore in Europa: **GDPR**, **NIS 2**, **Cyber Resilience Act (CRA)**.
2. Per ogni norma: ambito, chi riguarda, sanzioni, articoli rilevanti per il codice.
3. Distinguere **dato personale** da **dato anonimo** e capire quando GDPR si applica e quando no.
4. Riconoscere gli **obblighi di notifica** (72h GDPR, 24h NIS 2) e perché sono critici.
5. Collegare un **errore di codice** (es. SQL Injection) a una **norma violata** (es. GDPR Art. 32).
6. Avere coscienza che **scrivere codice insicuro non è solo cattiva qualità: in molti casi è illegale**.

## Materiale di riferimento

- `dispensa-sviluppo-sicuro-software.docx` → **Capitolo 2** (riusato integralmente)
- `dispensa_code_security_v8.docx` → **Capitolo 2** (per casi pratici e sanzioni in dettaglio)

## Articolazione oraria

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:10 | **4.1 Perché un programmatore deve sapere di leggi** — Il codice è soggetto a norme. Casi reali di multe miliardarie da bug software. | Frontale |
| 0:10 – 0:50 | **4.2 GDPR** — Cos'è, ambito territoriale (chiunque tratti dati di residenti UE). Articoli che riguardano il codice: **Art. 5** (principi), **Art. 25** (privacy by design e by default), **Art. 32** (sicurezza del trattamento), **Art. 33-34** (notifica breach 72h). Sanzioni fino a 20M€ o 4% fatturato. Casi: Equifax, British Airways, Marriott. | Frontale |
| 0:50 – 1:00 | **PAUSA** | |
| 1:00 – 1:35 | **4.3 NIS 2** — Direttiva 2022/2555. Chi riguarda (soggetti essenziali e importanti, lista in allegato). Obblighi: misure tecniche, governance, **notifica 24h** (early warning) + 72h + report finale 30gg. Sanzioni fino a 10M€ o 2% fatturato + responsabilità personale del management. | Frontale |
| 1:35 – 1:55 | **4.4 Cyber Resilience Act (CRA)** — Reg. 2024/2847, in vigore **dicembre 2027**. Cosa cambia: ogni "prodotto con elementi digitali" venduto in UE deve avere requisiti di cybersecurity by design, gestione vulnerabilità, supporto sicurezza per la durata di vita prevista. **Per gli sviluppatori cambia tutto**: la sicurezza è un requisito di mercato, non un nice-to-have. | Frontale |
| 1:55 – 2:00 | **4.5 Tabella riassuntiva** — Errore di codice → norma violata → multa potenziale. Da memorizzare. | Frontale |

## Tabella riassuntiva (da consegnare a fine modulo)

| Errore tecnico nel codice | Norma violata | Articolo | Sanzione potenziale |
|---------------------------|---------------|----------|---------------------|
| SQL Injection che espone dati personali | GDPR | Art. 5(1)(f), Art. 32 | Fino a 20M€ o 4% fatturato |
| Password salvate in chiaro o con MD5 | GDPR | Art. 32(1)(a) | Fino a 20M€ o 4% fatturato |
| Mancata notifica di un breach entro 72h | GDPR | Art. 33 | Fino a 10M€ o 2% fatturato |
| Vulnerabilità non gestita in software venduto | CRA | Art. 11, Art. 13 | Fino a 15M€ o 2,5% fatturato |
| Mancata segnalazione incidente "soggetto NIS 2" | NIS 2 | Art. 23 | Fino a 10M€ o 2% fatturato + responsabilità personale |
| Trattamento eccessivo (raccolta dati non necessari) | GDPR | Art. 5(1)(c) | Fino a 20M€ o 4% fatturato |

## Verifica

Le domande di M4 entrano in **V2 (verifica intermedia post M5)**.

Esempi:

- Cita 3 articoli del GDPR che riguardano direttamente chi scrive codice. Spiega cosa richiedono.
- Una banca italiana subisce un attacco. Entro quanto deve notificare al Garante? E all'autorità competente NIS 2?
- Una società di software vende a clienti UE un dispositivo IoT con backdoor. Da dicembre 2027 quale norma viola?
- Cos'è la "privacy by design"? Quale articolo del GDPR la richiede?

## Errori da evitare in classe

- **Non trasformare M4 in un corso di diritto** — focus su cosa cambia per chi scrive codice.
- **Non dire "sono cose da avvocati"** — il programmatore è coinvolto in prima persona nelle indagini post-breach. Il GDPR lo dice esplicitamente.
- **Non saltare CRA** — è la norma che cambierà di più la vita degli sviluppatori nei prossimi anni.

## Spunto opzionale (5 min se avanza tempo)

**Caso reale italiano**: provvedimento Garante Privacy 2023 — multa a una società italiana per password in chiaro nel database. Discussione: cosa avrebbe dovuto fare lo sviluppatore?
