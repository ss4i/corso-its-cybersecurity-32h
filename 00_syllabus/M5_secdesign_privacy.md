# M5 — Security & Privacy by Design (3h)

## Obiettivo

Al termine del modulo il discente sa:

1. Spiegare cosa significa **Security by Design** e in cosa differisce da "aggiungere sicurezza alla fine".
2. Applicare il framework **STRIDE** per fare threat modeling di un'applicazione.
3. Disegnare un **Data Flow Diagram** semplificato di un'app web e identificare i **trust boundary**.
4. Citare e spiegare i **7 principi** della Privacy by Design di Ann Cavoukian (recepiti da GDPR Art. 25).
5. Applicare **data minimization**, **pseudonimizzazione**, **anonimizzazione** a un dataset reale.
6. Sapere cos'è una **DPIA** (Data Protection Impact Assessment), quando è obbligatoria, cosa contiene.
7. Condurre un mini-threat-modeling **STRIDE su BancaPiccola** in gruppo.

## Materiale di riferimento

- Materiale nuovo: `01_materiali/M5_security_privacy_by_design.md` (creato per questo corso)
- `dispensa-sviluppo-sicuro-software.docx` → **Cap 1.4** (5 principi secure coding) come premessa
- `dispensa_code_security_v8.docx` → **Cap 3** (STRIDE in dettaglio) come riferimento

## Articolazione oraria

### Sessione — Security by Design (1.5h)

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:20 | **5.1 Security by Design — perché** — Aggiungere sicurezza dopo costa 10x-100x. Caso "Equifax patch ritardata". Lo "shift left". | Frontale |
| 0:20 – 0:35 | **5.2 Threat Modeling — cos'è** — Identificare minacce *prima* di scrivere codice. 4 domande: cosa stiamo costruendo? cosa può andare storto? cosa facciamo? abbiamo fatto un buon lavoro? | Frontale |
| 0:35 – 1:00 | **5.3 STRIDE** — Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation of privilege. Per ognuna: definizione, esempio, controllo tipico. | Frontale + esempi |
| 1:00 – 1:30 | **5.4 Data Flow Diagram + Trust Boundary** — come si disegna un DFD. Cosa sono i trust boundary. Esempio guidato su un'app di login. | Frontale + lavagna |

### Sessione — Privacy by Design (45 min)

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 1:30 – 1:35 | **PAUSA** | |
| 1:35 – 1:55 | **5.5 Privacy by Design — i 7 principi di Cavoukian** — proattivo non reattivo, privacy by default, embedded into design, full functionality, end-to-end security, visibility/transparency, respect for user privacy. Recepimento in GDPR Art. 25. | Frontale |
| 1:55 – 2:10 | **5.6 Data Minimization** in pratica — *raccogli il minimo necessario*. Esempio: form di iscrizione minimal vs maximal. | Frontale + esempio |
| 2:10 – 2:25 | **5.7 Pseudonimizzazione vs Anonimizzazione** — differenze tecniche e legali. K-anonymity, hashing irreversibile, mascheramento. Esempi. | Frontale |
| 2:25 – 2:40 | **5.8 DPIA in pillole** — quando è obbligatoria (Art. 35 GDPR), cosa contiene, chi la fa (DPO + sviluppo). Mini-template di 1 pagina. | Frontale |

### Sessione — Workshop pratico (45 min)

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 2:40 – 3:00 | **Lab M5 — STRIDE su BancaPiccola** (workshop in gruppi da 3) | **Lab in gruppo** |

## Lab del modulo (1h)

### Lab M5 — STRIDE su BancaPiccola

> **Nota**: il workshop occupa di fatto 45 min in aula, più 15 min di discussione collettiva. Totale ~1h.

**Setup**: piccoli gruppi (3 persone). Ogni gruppo riceve:

- Schema architetturale ad alto livello di BancaPiccola (browser → Flask → SQLite, autenticazione via cookie).
- Template DFD da completare (in `02_lab/M5_lab_stride_template.md`).
- Tabella STRIDE vuota da riempire.

**Consegna** (45 min):

1. Disegnate il DFD con:
   - Entità esterne (utente)
   - Processi (login, lista fatture, dettaglio fattura)
   - Datastore (DB SQLite)
   - Flussi
   - **Trust boundary** (almeno il browser → server)
2. Per ogni elemento, identificate **almeno 2 minacce STRIDE** (focus su Spoofing, Tampering, Information disclosure).
3. Per ogni minaccia, proponete **una difesa**.

**Discussione collettiva** (15 min): ogni gruppo presenta una minaccia trovata. Il docente sintetizza alla lavagna i pattern.

**Output**: una tabella per gruppo, consegnata. Vale come parte di V2.

## Verifica

Le domande di M5 entrano in **V2 (verifica intermedia post M5)**.

Esempi:

- Cosa significa "shift left" della sicurezza?
- Spiega la differenza tra Tampering e Repudiation. Per ognuna fai un esempio in BancaPiccola.
- Cita 3 dei 7 principi di Cavoukian e spiegali.
- Quando una DPIA è obbligatoria? Cita 2 casi.
- Differenza tra pseudonimizzazione e anonimizzazione: chi protegge di più? Quale è reversibile?

## Errori da evitare in classe

- **Non far diventare STRIDE un esercizio di nomenclatura** — il valore è nel processo (4 domande), non nelle 6 lettere.
- **Non confondere security e privacy** — sovrapposte ma distinte. Privacy = controllo dell'individuo sui propri dati; Security = protezione delle proprietà del sistema. Esempi: si può avere security senza privacy (es. sorveglianza di stato sicura) e privacy senza security (es. lettera anonima persa).
- **Non saltare il workshop**: è il primo momento del corso in cui i discenti applicano un metodo strutturato. Vale più di un'ora di lezione frontale.
