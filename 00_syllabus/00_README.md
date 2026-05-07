# Corso ITS — Cybersecurity e Sicurezza delle Applicazioni

**Durata:** 32 ore
**Prerequisiti:** nessuno (corso pensato per discenti senza preparazione tecnica)
**Linguaggio di laboratorio:** Python 3.12 (Flask, requests, socket, scapy)
**Sistema operativo di lavoro:** Windows / macOS / Linux (i lab funzionano su tutti)
**Docente:** Ing. Alessandro Manneschi
**Edizione:** Anno Formativo 2024/2025

---

## 1. Finalità del corso

Al termine del corso il discente sa:

1. **Spiegare** cos'è la cybersecurity, quali sono le minacce più comuni e quali principi guidano una difesa efficace.
2. **Riconoscere** come funziona la comunicazione in rete (modello ISO/OSI, TCP/IP) e identificare le principali vulnerabilità a ogni livello.
3. **Leggere e scrivere** richieste HTTP/HTTPS, comprendere headers e codici di stato, individuare gli header di sicurezza.
4. **Inquadrare** il quadro normativo europeo (GDPR, NIS 2, Cyber Resilience Act) e collegare un errore di codice a una norma violata.
5. **Applicare** i principi di Security by Design e Privacy by Design fin dalla progettazione di un'applicazione.
6. **Identificare e correggere** le 5 vulnerabilità web più diffuse: SQL Injection, IDOR/Broken Access Control, Cryptographic Failures, XSS, Path Traversal.
7. **Usare strumenti professionali**: Wireshark, DevTools, `pip-audit`, Burp (cenno), oltre a script Python autoprodotti per scanning e testing.

## 2. Approccio didattico

- **Zero prerequisiti**: si parte dall'installazione di Python e dall'apertura del terminale.
- **Passo passo**: ogni concetto è introdotto con un'analogia concreta, poi visto in pratica, poi formalizzato.
- **Lab guidati**: ogni modulo tecnico ha un laboratorio dove il discente scrive/esegue codice. Il docente segue dal vivo.
- **Errore come strumento**: si fa "rompere" l'applicazione vulnerabile, poi si ripara. Si impara molto di più così che leggendo la difesa per prima.
- **Bilanciamento**: 14h di teoria, 18h di laboratorio (rapporto ~45/55).

## 3. Ripartizione delle 32 ore

| # | Modulo | Ore | Teoria | Lab |
|---|--------|-----|--------|-----|
| **M0** | Setup ambiente di lavoro | 2 | 0,5 | 1,5 |
| **M1** | Fondamenti di Cybersecurity | 4 | 3 | 1 |
| **M2** | Networking & ISO/OSI (Wireshark + protocolli) | 6 | 3 | 3 |
| **M3** | Protocollo HTTP | 4 | 2 | 2 |
| **M4** | Quadro Normativo (GDPR, NIS 2, CRA) | 2 | 2 | 0 |
| **M5** | Security & Privacy by Design | 3 | 2 | 1 |
| **M6** | Sicurezza delle Applicazioni Web | 9 | 3 | 6 |
| **M7** | Lab integrato + chiusura | 2 | 0 | 2 |
| | **Totale** | **32** | **15,5** | **16,5** |

## 4. Materiali del corso

### Dispense di riferimento (esistenti)

- **Dispensa principale:** `dispensa-sviluppo-sicuro-software.docx` (Cap 0 → Cap 10)
- **HTTP:** `Dispensa_HTTP_ITS_v2_Prodigi.docx`
- **Pentest (per esempi/casi):** `dispensa-pentest-its_6.docx`

### Materiali nuovi prodotti per questo corso

Sono in `Corso_32h/01_materiali/`:

- `M2_networking_isoosi.md` — Pila ISO/OSI, protocolli, vulnerabilità, Wireshark
- `M5_security_privacy_by_design.md` — STRIDE, 7 principi PbD, DPIA in pillole
- `M1_fondamenti_cybersecurity.md` — Adattamento Cap 1 a 4h con CIA triad e tassonomia minacce

### Laboratori

In `Corso_32h/02_lab/` — script Python pronti, dataset di test, soluzioni separate.

### Test e verifiche

In `Corso_32h/03_test/`:

- **V1** — Verifica intermedia dopo M3 (Cybersecurity + Networking + HTTP)
- **V2** — Verifica intermedia dopo M5 (Normativa + Security/Privacy by Design)
- **V_FINALE** — Verifica finale post M7 (tutto + casi pratici)

Soluzioni in file separati con suffisso `_soluzioni`.

## 5. Sistema di valutazione

| Componente | Peso | Quando |
|------------|------|--------|
| Verifica intermedia 1 | 25% | Fine M3 (10h) |
| Verifica intermedia 2 | 20% | Fine M5 (19h) |
| Lab integrato (M7) | 20% | Fine corso |
| Verifica finale scritta | 35% | Fine corso |

**Soglia di sufficienza:** 60/100. Il lab integrato è obbligatorio (consegna scritta).

## 6. Strumenti software richiesti

Tutti gratuiti, installati nel **Modulo M0**:

| Strumento | A cosa serve | Quando lo installiamo |
|-----------|--------------|------------------------|
| Python 3.12 | Linguaggio dei lab | M0 |
| Visual Studio Code | Editor | M0 |
| Git | Scaricare BancaPiccola | M0 |
| DB Browser for SQLite | Ispezionare i database | M0 |
| Browser moderno + DevTools | Lab HTTP e XSS | M0 |
| **Wireshark** | Analisi traffico di rete | M2 |
| **curl** o REST Client (estensione VSCode) | Lab HTTP/API | M3 |
| `pip-audit` | Lab supply chain | M6.6 |

## 7. Calendario tipico (suggerimento)

Distribuzione su **8 incontri da 4 ore** ciascuno:

| Incontro | Contenuti |
|----------|-----------|
| **G1 (4h)** | M0 (2h) + M1 prima parte (2h) |
| **G2 (4h)** | M1 seconda parte (2h) + M2 prima parte (2h) |
| **G3 (4h)** | M2 seconda parte (4h) |
| **G4 (4h)** | M3 (4h) + **V1** alla fine |
| **G5 (4h)** | M4 (2h) + M5 prima parte (2h) |
| **G6 (4h)** | M5 seconda parte (1h) + M6 prima parte (3h) — **V2 inizio** |
| **G7 (4h)** | M6 seconda parte (4h) |
| **G8 (4h)** | M6 chiusura (2h) + M7 lab integrato (2h) — **V_FINALE** alla fine |

> Adattabile a 16 incontri da 2h o a un corso intensivo di 4 giorni pieni (8h/giorno).

## 8. Indice file del corso

```
Corso_32h/
├── 00_syllabus/
│   ├── 00_README.md                  ← questo file
│   ├── M0_setup.md
│   ├── M1_fondamenti.md
│   ├── M2_networking.md
│   ├── M3_http.md
│   ├── M4_normativa.md
│   ├── M5_secdesign_privacy.md
│   ├── M6_applicazioni_web.md
│   └── M7_lab_integrato.md
├── 01_materiali/
│   ├── M1_fondamenti_cybersecurity.md
│   ├── M2_networking_isoosi.md
│   └── M5_security_privacy_by_design.md
├── 02_lab/
│   ├── M2_lab1_socket_tcp.py
│   ├── M2_lab2_port_scanner.py
│   ├── M2_lab3_scapy_sniff.py
│   └── M5_lab_stride_template.md
├── 03_test/
│   ├── V1_intermedia_post_M3.md
│   ├── V1_soluzioni.md
│   ├── V2_intermedia_post_M5.md
│   ├── V2_soluzioni.md
│   ├── V_FINALE.md
│   └── V_FINALE_soluzioni.md
└── 04_slide/                          ← (da produrre in seconda fase, opzionale)
```
