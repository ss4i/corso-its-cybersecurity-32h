# Corso ITS — Cybersecurity e Sicurezza delle Applicazioni

**Versione**: 1.0 — 2026-05-06
**Durata base**: 32 ore (estendibile a 64h con moduli EXTRA)
**Livello**: principiante → intermedio
**Linguaggio lab**: Python 3.12 (Flask, FastAPI, Pydantic, scapy)
**Autore**: Ing. Alessandro Manneschi
**Istituzioni**: ITS Prodigi · ITS Empoli · SS4I S.r.l.

---

## 1. Cosa contiene questo corso

Un corso ITS completo di **cybersecurity e sicurezza applicativa** per discenti **senza preparazione tecnica**:

- **8 moduli core** (M0-M7) per 32 ore di lezione
- **6 moduli EXTRA** per aggiungere fino a 21h di approfondimento
- **9 laboratori Python** pronti all'uso
- **3 verifiche standard + 6 verifiche EXTRA** con soluzioni
- **14 set di slide** (PowerPoint generate con pandoc)
- Tutto disponibile in **markdown** + **docx** + **pptx**

---

## 2. Struttura della cartella

```
Corso_32h/
├── README.md                          ← questo file (mappa generale)
├── README_CALENDARIO.md               ← calendario operativo per docente
│
├── 00_syllabus/                       ← Programma dei moduli (per docente)
│   ├── 00_README.md                   ← syllabus generale
│   ├── M0_setup.md                    ← syllabus modulo M0
│   ├── M1_fondamenti.md
│   ├── M2_networking.md
│   ├── M3_http.md
│   ├── M4_normativa.md
│   ├── M5_secdesign_privacy.md
│   ├── M6_applicazioni_web.md
│   └── M7_lab_integrato.md
│
├── 01_materiali/                      ← Dispense didattiche (per studenti)
│   ├── README.md                      ← guida CORE vs EXTRA
│   │
│   ├── M0_setup_ambiente.md           ← CORE — 8 dispense
│   ├── M1_fondamenti_cybersecurity.md
│   ├── M2_networking_isoosi.md
│   ├── M3_http.md
│   ├── M4_normativa.md
│   ├── M5_security_privacy_by_design.md
│   ├── M6_applicazioni_web.md
│   ├── M7_lab_integrato.md
│   │
│   ├── M_EXTRA_jwt_oauth_csrf.md      ← EXTRA — 6 moduli avanzati
│   ├── M_EXTRA_api_security.md
│   ├── M_EXTRA_input_validation.md
│   ├── M_EXTRA_strumenti_enterprise.md
│   ├── M_EXTRA_ai_llm_security.md
│   └── M_EXTRA_logging_monitoring.md
│
├── 02_lab/                            ← Laboratori Python
│   ├── M2.2_socket_tcp.py             ← CORE — 4 lab
│   ├── M2.3_port_scanner.py
│   ├── M2.4_scapy_sniff.py
│   ├── M3.2_http_client.py
│   ├── M5_lab_stride_template.md
│   │
│   ├── M_EXTRA_jwt_lab.py             ← EXTRA — 5 lab + 1 sotto-progetto
│   ├── M_EXTRA_api_security_lab.py
│   ├── M_EXTRA_input_validation_lab.py
│   ├── M_EXTRA_llm_chatbot_lab.py
│   ├── M_EXTRA_logging_lab.py
│   └── M_EXTRA_devsecops_lab/         ← sotto-progetto completo
│       ├── README.md
│       ├── app.py                     ← app Flask vulnerabile
│       ├── requirements.txt
│       ├── Dockerfile
│       ├── .github/workflows/security.yml
│       ├── .pre-commit-config.yaml
│       └── solution/                  ← versione corretta
│
├── 03_test/                           ← Verifiche
│   ├── V1_intermedia_post_M3.md       ← CORE — V1 (post M3)
│   ├── V1_soluzioni.md
│   ├── V2_intermedia_post_M5.md       ← CORE — V2 (post M5)
│   ├── V2_soluzioni.md
│   ├── V_FINALE.md                    ← CORE — V_FINALE
│   ├── V_FINALE_soluzioni.md
│   │
│   ├── V_EXTRA_jwt.md                 ← EXTRA — 6 verifiche
│   ├── V_EXTRA_jwt_soluzioni.md
│   ├── V_EXTRA_api.md
│   ├── V_EXTRA_api_soluzioni.md
│   ├── V_EXTRA_validation.md
│   ├── V_EXTRA_validation_soluzioni.md
│   ├── V_EXTRA_devsecops.md
│   ├── V_EXTRA_devsecops_soluzioni.md
│   ├── V_EXTRA_aillm.md
│   ├── V_EXTRA_aillm_soluzioni.md
│   ├── V_EXTRA_logging.md
│   └── V_EXTRA_logging_soluzioni.md
│
├── 04_slide/                          ← Slide PowerPoint
│   ├── M0_slide_setup.md/.pptx        ← CORE — 8 slide kit
│   ├── M1_slide_fondamenti.md/.pptx
│   ├── ...
│   ├── M7_slide_lab_integrato.md/.pptx
│   │
│   ├── M_EXTRA_jwt_oauth_csrf.md/.pptx     ← EXTRA — 6 slide kit
│   ├── M_EXTRA_api_security.md/.pptx
│   ├── ...
│   └── M_EXTRA_logging_monitoring.md/.pptx
│
└── docx/                              ← conversioni docx di tutto
    ├── 00_syllabus/
    ├── 01_materiali/
    ├── 02_lab/
    └── 03_test/
```

---

## 3. Tre modi di usare il corso

### 3.1 — Corso 32h base ("first course")

Per ITS al primo anno, primo contatto con cybersecurity.

**Materiali da usare**:
- Tutti i CORE M0-M7 (`01_materiali/M*.md`)
- Lab CORE (`02_lab/M2.*.py`, `M3.2.py`, `M5_lab_stride_template.md`)
- Test CORE (V1, V2, V_FINALE)
- Slide CORE (M0-M7 in `04_slide/`)

**Cosa NON usare**:
- Tutti i moduli `M_EXTRA_*` (sono per il secondo anno o per chi vuole approfondire).

**Output**: studente sa riconoscere e correggere SQL Injection, IDOR, password deboli, XSS, supply chain, path traversal. Conosce GDPR/NIS2/CRA. Sa fare un threat modeling con STRIDE.

### 3.2 — Corso 32h "moderno 2026" (raccomandato)

Stessa durata, ma con **rebalancing** per coprire anche AI security e input validation.

| Modulo | Ore originali | Ore raccomandate | Modifica |
|--------|----------------|-------------------|----------|
| M0 | 2 | 2 | invariato |
| M1 | 4 | 3 | -1h (casi reali come homework) |
| M2 | 6 | 5 | -1h (vuln protocollo come homework) |
| M3 | 4 | 4 | + lettura `M_EXTRA_jwt_oauth_csrf` |
| M4 | 2 | 2 | invariato |
| M5 | 3 | 3 | invariato |
| M6 | 9 | 9 | + 1h M6.0 da `M_EXTRA_input_validation` (-1h SQLi) |
| M7 | 2 | 2 | invariato |
| **+M8 NUOVO** | — | **2h** | AI/LLM Security base (cap 1-3 di EXTRA AI/LLM) |
| **TOTALE** | 32 | **32** | bilanciato |

### 3.3 — Corso 64h "completo" (32h base + 32h avanzato)

Per ITS al secondo anno o specializzazione.

**32h base**: come 3.1.
**32h avanzato** (16 lezioni × 2h):

| Settimana | Argomento |
|-----------|-----------|
| 1 | EXTRA Input Validation (3h) |
| 2 | EXTRA JWT/OAuth/CSRF parte 1 (2h) |
| 3 | EXTRA JWT/OAuth/CSRF parte 2 (2h) |
| 4 | EXTRA API Security parte 1 (2h) |
| 5 | EXTRA API Security parte 2 (2h) |
| 6 | EXTRA AI/LLM Security parte 1 (2h) |
| 7 | EXTRA AI/LLM Security parte 2 (2h) |
| 8 | EXTRA Strumenti Enterprise parte 1 (2h) |
| 9 | EXTRA Strumenti Enterprise parte 2 + DevSecOps Lab (3h) |
| 10 | EXTRA Logging & Monitoring (2h) |
| 11 | Lab integrato avanzato (BancaPiccola+JWT+API+LLM) (3h) |
| 12 | V_EXTRA finale (2h) |

Vedi `README_CALENDARIO.md` per dettagli e timing settimanale.

---

## 4. Sistema di valutazione

### 4.1 — Corso 32h base

| Componente | Peso | Quando |
|------------|------|--------|
| V1 (post M3) | 25% | Fine settimana 4 |
| V2 (post M5) | 20% | Fine settimana 6 |
| Lab integrato M7 | 20% | Fine corso |
| V_FINALE | 35% | Fine corso |

**Soglia sufficienza**: 60/100.

### 4.2 — Corso 64h

| Componente | Peso |
|------------|------|
| V1 + V2 (32h base) | 25% |
| Lab integrato M7 | 15% |
| V_FINALE 32h base | 20% |
| V_EXTRA selezionata (3 su 6) | 15% |
| Lab DevSecOps + report | 15% |
| Esame finale orale | 10% |

---

## 5. Strumenti software

### 5.1 — Necessari (corso base, M0-M7)

| Tool | Quando | Note |
|------|--------|------|
| Python 3.12+ | M0 | obbligatorio |
| Visual Studio Code | M0 | con estensione Python |
| Git | M0 | per clonare BancaPiccola |
| DB Browser for SQLite | M0 | per ispezione DB |
| Browser moderno | tutti | Chrome/Edge/Firefox + DevTools |
| **Wireshark** | M2 | con Npcap (Windows) |
| **scapy** | M2 | `pip install scapy` |
| **curl** | M3 | incluso in Windows 10+ |
| **bcrypt, requests, flask** | M6 | `pip install` |
| **pip-audit** | M6.6 | `pip install pip-audit` |

### 5.2 — Aggiuntivi (corso 64h con EXTRA)

| Tool | Modulo | Note |
|------|--------|------|
| **FastAPI, Pydantic[email]** | EXTRA API | `pip install` |
| **PyJWT** | EXTRA JWT | `pip install` |
| **bleach** | EXTRA Input Validation | `pip install` |
| **bandit** | EXTRA DevSecOps | `pip install` |
| **gitleaks** | EXTRA DevSecOps | binary download |
| **trivy** | EXTRA DevSecOps | binary o `brew install` |
| **OpenAI Python SDK** | EXTRA AI/LLM | `pip install openai` (richiede API key) |
| **Garak** (opzionale) | EXTRA AI/LLM | `pip install garak` per red teaming |
| **Docker Desktop** | EXTRA DevSecOps | per container scan |

---

## 6. Per il docente — checklist d'uso

### Prima del corso (≥1 settimana)

- [ ] Leggi `00_syllabus/00_README.md`
- [ ] Leggi i syllabus M0-M7
- [ ] Leggi i materiali CORE
- [ ] Decidi se aggiungere EXTRA (modalità 3.2 o 3.3)
- [ ] **Testa i lab sull'aula reale** (Wireshark, scapy, Flask)
- [ ] Verifica `BancaPiccola-vuln/` e `BancaPiccola-secure/`
- [ ] Stampa il "ground truth" di M7 cap 5
- [ ] Predisponi una **VM Linux** di backup pronta (se i lab Windows hanno problemi)

### Durante il corso

- [ ] Segui i syllabus per il timing
- [ ] Distribuisci materiali (`01_materiali/`) come dispense
- [ ] Proietta slide (`04_slide/*.pptx`)
- [ ] Guida i lab (`02_lab/`)
- [ ] Somministra V1 a fine M3, V2 a fine M5, V_FINALE a fine corso
- [ ] Valuta lab M7 con la griglia

### Dopo il corso

- [ ] Distribuisci EXTRA come letture per chi vuole approfondire
- [ ] Raccogli feedback discenti
- [ ] Aggiorna CVE/casi se >6 mesi (vedi sezione manutenzione)

---

## 7. Manutenzione

| Frequenza | Cosa rivedere |
|-----------|----------------|
| **Annuale** | OWASP Top 10 (versione corrente) |
| **Annuale** | OWASP API Security Top 10 |
| **Annuale** | OWASP LLM Top 10 (cambia ogni anno) |
| **Trimestrale** | CVE citate (es. CVE-2024-3094 → obsoleta nel 2027) |
| **Annuale** | Casi italiani Garante Privacy (nuovi provvedimenti) |
| **Quando cambiano** | NIS 2 transposition, CRA secondary acts, EU AI Act |
| **Annuale** | Tool list (sempre nuovi DAST/SAST/SCA) |
| **Annuale** | Riferimenti normativi UE (italiani) |

---

## 8. Per lo studente — come orientarti

### Prima di iniziare

1. Apri `01_materiali/M0_setup_ambiente.md` e installa l'ambiente.
2. Verifica con il "checklist di sopravvivenza" alla fine.

### Durante un modulo

1. Leggi il materiale dispensa (`01_materiali/M*.md`).
2. Segui le slide proiettate dal docente.
3. Esegui i lab (`02_lab/`) **con il docente** la prima volta.
4. Rifai i lab a casa per consolidare.
5. Studia per la verifica.

### Per approfondire

1. Sezione "Per approfondire" alla fine di ogni dispensa.
2. EXTRA del modulo corrispondente (`M_EXTRA_*`).
3. Risorse esterne: PortSwigger Academy, OWASP, TryHackMe.

### Per esercitarsi

1. Lab del corso, rifatti senza guida.
2. Lab DevSecOps avanzato (`02_lab/M_EXTRA_devsecops_lab/`).
3. Mini-CTF: `BancaPiccola-vuln`.

---

## 9. Numeri chiave

```
8 moduli CORE                            32h base
+ 6 moduli EXTRA                         + 18-21h
= 8 + 6 = 14 dispense                    ~80h materiale totale

9 laboratori Python (eseguibili)
3 verifiche CORE + 6 EXTRA               9 verifiche con soluzioni
14 slide kit (.md + .pptx)
1 lab integrato finale (BancaPiccola)
1 sotto-progetto DevSecOps completo

~50 file markdown
~30 file docx (conversione)
~14 file pptx (conversione)
~10 file Python (lab)
```

---

## 10. Crediti & contatti

- **Autore**: Ing. Alessandro Manneschi (alessandro.manneschi@gmail.com)
- **Istituzioni**: ITS Prodigi (Empoli), SS4I S.r.l.
- **Anno formativo**: 2024/2025
- **Versione**: 1.0
- **Licenza**: il materiale può essere usato per fini didattici interni

Per:
- **Errori, refusi**: aprire issue o contattare via email
- **Suggerimenti**: feedback dopo ogni edizione del corso
- **Contributi**: pull request benvenute

---

## 11. Cambia log

| Data | Versione | Cosa è cambiato |
|------|----------|-----------------|
| 2026-05-06 | 1.0 | Prima versione completa con CORE + EXTRA |

---

## 12. Risorse esterne raccomandate

### Per il docente

- **OWASP**: https://owasp.org (Top 10, ASVS, cheat sheets)
- **NIST CSRC**: https://csrc.nist.gov (SSDF, frameworks)
- **MITRE ATT&CK & ATLAS**: https://attack.mitre.org, https://atlas.mitre.org
- **Garante Privacy**: https://www.garanteprivacy.it (provvedimenti italiani)
- **ENISA**: https://www.enisa.europa.eu (cybersecurity UE)

### Per gli studenti (gratuiti)

- **PortSwigger Web Security Academy** — gold standard, lab gratuiti
- **TryHackMe** — rooms beginner-friendly
- **HackTheBox starting point**
- **OverTheWire Bandit** — Linux + sec
- **OWASP** — cheat sheets
- **roadmap.sh** — roadmap di apprendimento cybersec

### Certificazioni "entry"

- **CompTIA Security+** (vendor neutral, ~150€)
- **eJPT** (eLearnSecurity, hands-on)
- **PortSwigger BSCP** (Burp/AppSec)

---

> **Buona strada.**
> *— Ing. Alessandro Manneschi*
