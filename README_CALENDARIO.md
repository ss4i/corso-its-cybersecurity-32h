# Calendario operativo del corso

**Versione**: 1.0
**Per**: docenti del corso ITS Cybersecurity (32h base + EXTRA)

> Questo documento fornisce calendari pronti per **3 modalità** di erogazione, con timing dettagliato per ogni ora di lezione, materiale da preparare prima e attività in aula.

---

## Indice

- [1. Modalità A — 32h base, 8 incontri × 4h](#mod-a)
- [2. Modalità B — 32h base, 16 incontri × 2h](#mod-b)
- [3. Modalità C — 32h base intensivo, 4 giorni × 8h](#mod-c)
- [4. Modalità D — 64h (32h base + 32h avanzato EXTRA)](#mod-d)
- [5. Note operative comuni](#note)

---

<a name="mod-a"></a>
## 1. Modalità A — 32h base, 8 incontri × 4h

> Schema "standard" raccomandato. 8 settimane, una lezione di 4 ore (con pausa).

### Settimana 1 — G1 (4h): Setup + M1 prima parte

| Tempo | Argomento | File da preparare |
|-------|-----------|-------------------|
| 09:00–09:15 | Introduzione corso, presentazioni | README.md, slide M0 |
| 09:15–11:00 | **M0 — Setup ambiente** (Python, VS Code, terminale, venv, Flask) | `M0_setup_ambiente.md` + lab live |
| 11:00–11:15 | **PAUSA** | |
| 11:15–13:00 | **M1.1-1.4 — Fondamenti**: cybersec vs codice, CIA Triad, tassonomia minacce | `M1_fondamenti_cybersecurity.md` cap 1-3, slide M1 |

**Compito a casa**: completare setup (Git, DB Browser, clone BancaPiccola).
**Verifica inizio G2**: tutti hanno `(.venv)` attivo + Flask hello mondo OK.

---

### Settimana 2 — G2 (4h): M1 fine + M2 prima parte

| Tempo | Argomento |
|-------|-----------|
| 09:00–09:15 | Verifica setup compiti casa, recupero |
| 09:15–11:00 | **M1.5-1.6 — Casi reali, mentalità avversaria, 5 principi** + Lab a coppie |
| 11:00–11:15 | **PAUSA** |
| 11:15–13:00 | **M2.1-2.6 — Networking**: ISO/OSI, Ethernet, ARP, IP, ICMP, TCP |

**Materiali**: `M1_fondamenti_cybersecurity.md` cap 4-7, `M2_networking_isoosi.md` cap 1-6, slide M1 + M2.
**Compito a casa**: scaricare e installare Wireshark.

---

### Settimana 3 — G3 (4h): M2 lab Wireshark + Python

| Tempo | Argomento |
|-------|-----------|
| 09:00–10:00 | **M2.7-2.8 — Livelli 5-7**: DNS, TLS, HTTP overview, vulnerabilità |
| 10:00–10:45 | **Lab M2.1 — Wireshark Discovery** |
| 10:45–11:00 | **PAUSA** |
| 11:00–11:30 | **Lab M2.2 — Socket TCP Python** |
| 11:30–12:00 | **Lab M2.3 — Port Scanner** |
| 12:00–12:30 | **Lab M2.4 — Scapy Sniff** |
| 12:30–13:00 | Sintesi M2 + domande |

**Materiali**: `M2_networking_isoosi.md` cap 7-11, lab in `02_lab/M2.*.py`.

> ⚠️ **Test ambiente in anticipo**: il giorno prima testare Wireshark e scapy su 1-2 PC dell'aula. Su Windows con antivirus enterprise spesso falliscono.

---

### Settimana 4 — G4 (4h): M3 HTTP + V1

| Tempo | Argomento |
|-------|-----------|
| 09:00–09:30 | **M3.1-3.2 — HTTP**: ripasso + URL/metodi |
| 09:30–10:30 | **M3.3-3.7 — Status code, header, header di sicurezza** |
| 10:30–10:45 | **PAUSA** |
| 10:45–11:30 | **Lab M3.1 — DevTools Discovery** |
| 11:30–12:00 | **M3.5 — Cookie sicuri (Secure, HttpOnly, SameSite) + HTTPS/TLS** |
| 12:00–12:15 | **Lab M3.2 — `requests` Python** |
| 12:15–13:00 | **🟦 V1 — Verifica intermedia (60 min)** |

**Materiali**: `M3_http.md` completo, slide M3, `02_lab/M3.2_http_client.py`.
**Output**: V1 corretta nei 3 giorni successivi → distribuita prima di G5.

---

### Settimana 5 — G5 (4h): M4 Normativa + M5 prima parte

| Tempo | Argomento |
|-------|-----------|
| 09:00–10:00 | **M4 — GDPR** (articoli 5, 25, 32, 33-34, 35) |
| 10:00–10:30 | **M4 — NIS 2** + casi italiani |
| 10:30–10:45 | **PAUSA** |
| 10:45–11:00 | **M4 — CRA + tabella errore→norma** |
| 11:00–12:00 | **M5.1-5.4 — Security by Design**: shift left, STRIDE, DFD |
| 12:00–13:00 | **M5.5-5.7 — Privacy by Design**: 7 principi Cavoukian, data minimization, pseudo/anon |

**Materiali**: `M4_normativa.md`, `M5_security_privacy_by_design.md` cap 1-7.

---

### Settimana 6 — G6 (4h): M5 fine + M6 prima parte + V2

| Tempo | Argomento |
|-------|-----------|
| 09:00–09:30 | **M5.8 — DPIA** + cenni |
| 09:30–10:30 | **🟧 Lab M5 — Workshop STRIDE su BancaPiccola** (3 gruppi × 30 min) |
| 10:30–10:45 | **PAUSA** |
| 10:45–11:30 | **🟦 V2 — Verifica intermedia (50 min)** |
| 11:30–12:00 | **M6.1 — OWASP Top 10:2025 + CVE/CVSS** |
| 12:00–13:00 | **M6.2 — SQL Injection (parte 1)**: introduzione + costruzione `bancapiccola-mini` |

**Materiali**: `M5_secdesign_privacy.md` cap 8-9, `M6_applicazioni_web.md` cap 1-3.

---

### Settimana 7 — G7 (4h): M6 cuore tecnico

| Tempo | Argomento |
|-------|-----------|
| 09:00–09:30 | **M6.2 — SQLi (parte 2)**: attacco UNION + correzione |
| 09:30–11:00 | **M6.3 — Broken Access Control / IDOR** + lab |
| 11:00–11:15 | **PAUSA** |
| 11:15–12:30 | **M6.4 — Password & crittografia** + lab bcrypt |
| 12:30–13:00 | **M6.5 — XSS (parte 1)**: 3 tipi + reflected XSS |

**Materiali**: `M6_applicazioni_web.md` cap 4.1-4.5.

---

### Settimana 8 — G8 (4h): M6 fine + M7 + V_FINALE

| Tempo | Argomento |
|-------|-----------|
| 09:00–10:00 | **M6.5 — XSS (parte 2)**: stored XSS + difese (escape, CSP) |
| 10:00–10:30 | **M6.6 — Supply Chain**: pip-audit lab |
| 10:30–11:00 | **M6.7 — Path Traversal** + lab |
| 11:00–11:15 | **PAUSA** |
| 11:15–11:30 | Briefing M7 |
| 11:30–12:45 | **🟧 M7 — Lab Integrato (75 min lavoro)** |
| 12:45–13:00 | Discussione collettiva + chiusura corso |

**Output**:
- Report M7 da consegnare (1-2 pagine)
- **🟦 V_FINALE** somministrata in giorno separato (90 min) o online

---

<a name="mod-b"></a>
## 2. Modalità B — 32h base, 16 incontri × 2h

> Per scuole serali o moduli "spalmati". 16 settimane, 1 lezione di 2h.

| # | Settimana | Argomento (2h) |
|---|-----------|----------------|
| 1 | Settimana 1 | M0 setup completo |
| 2 | Settimana 2 | M1.1-1.4 fondamenti, CIA, tassonomia |
| 3 | Settimana 3 | M1.5-1.6 casi reali + 5 principi + lab "cosa è andato storto" |
| 4 | Settimana 4 | M2.1-2.6 ISO/OSI livelli 1-4 |
| 5 | Settimana 5 | M2.7-2.8 livelli 5-7 + Lab Wireshark M2.1 |
| 6 | Settimana 6 | Lab Python M2.2 + M2.3 + M2.4 |
| 7 | Settimana 7 | M3.1-3.5 HTTP, status, header |
| 8 | Settimana 8 | M3.6-3.8 header sicurezza + cookie + TLS + Lab M3 + **🟦 V1** |
| 9 | Settimana 9 | M4 normativa completa |
| 10 | Settimana 10 | M5.1-5.4 STRIDE + DFD |
| 11 | Settimana 11 | M5.5-5.8 Privacy by Design + workshop STRIDE + **🟦 V2** |
| 12 | Settimana 12 | M6.1 OWASP + M6.2 SQLi (parte 1) |
| 13 | Settimana 13 | M6.2 SQLi (parte 2) + M6.3 IDOR |
| 14 | Settimana 14 | M6.4 Crypto + M6.5 XSS |
| 15 | Settimana 15 | M6.6 Supply Chain + M6.7 Path Traversal |
| 16 | Settimana 16 | **🟧 M7 Lab Integrato** + chiusura + **🟦 V_FINALE** |

---

<a name="mod-c"></a>
## 3. Modalità C — 32h intensivo, 4 giorni × 8h

> Per bootcamp, summer school. 4 giorni full immersive (08:30-17:30 con pausa pranzo).

### Giorno 1 — Fondamenti & Networking

| Ora | Argomento |
|-----|-----------|
| 08:30–10:30 | M0 setup + M1.1-1.3 |
| 10:30–10:45 | pausa |
| 10:45–12:30 | M1.4-1.6 + Lab M1 |
| 12:30–13:30 | **PRANZO** |
| 13:30–15:30 | M2.1-2.6 ISO/OSI |
| 15:30–15:45 | pausa |
| 15:45–17:30 | M2.7-2.8 + Lab Wireshark + Lab Python |

### Giorno 2 — HTTP & Normativa

| Ora | Argomento |
|-----|-----------|
| 08:30–10:30 | M3.1-3.5 HTTP |
| 10:30–10:45 | pausa |
| 10:45–12:30 | M3.6-3.8 header sicurezza + cookie + Lab M3 |
| 12:30–13:30 | **PRANZO** |
| 13:30–14:30 | **🟦 V1 verifica** |
| 14:30–16:00 | M4 normativa |
| 16:00–16:15 | pausa |
| 16:15–17:30 | M5.1-5.4 Security by Design |

### Giorno 3 — Privacy + Cuore tecnico

| Ora | Argomento |
|-----|-----------|
| 08:30–10:00 | M5.5-5.8 + Workshop STRIDE |
| 10:00–10:15 | pausa |
| 10:15–11:30 | **🟦 V2 verifica** |
| 11:30–12:30 | M6.1 OWASP + M6.2 SQLi parte 1 |
| 12:30–13:30 | **PRANZO** |
| 13:30–15:00 | M6.2 SQLi parte 2 + M6.3 IDOR |
| 15:00–15:15 | pausa |
| 15:15–17:30 | M6.4 Crypto + M6.5 XSS |

### Giorno 4 — Difese finali + Lab integrato

| Ora | Argomento |
|-----|-----------|
| 08:30–10:00 | M6.6 Supply Chain + M6.7 Path Traversal |
| 10:00–10:15 | pausa |
| 10:15–12:30 | **🟧 M7 Lab Integrato (75+45 min lavoro+discussione)** |
| 12:30–13:30 | **PRANZO** |
| 13:30–15:00 | **🟦 V_FINALE verifica** |
| 15:00–15:15 | pausa |
| 15:15–17:00 | Correzione collettiva + chiusura corso + Q&A |
| 17:00–17:30 | Cerimonia di chiusura, attestati |

> **Avvertenza**: l'intensivo è faticoso. Slow down se la classe sta annaspando. Meglio togliere M6.7 e fare M7 con calma, che fare tutto a metà.

---

<a name="mod-d"></a>
## 4. Modalità D — 64h totale (32h base + 32h avanzato)

> Per ITS al II anno o specializzazione. Erogabile come **32h base** (vedi sopra) **+ 32h avanzato** (12 settimane × 2-3h).

### 32h avanzato — 12 lezioni

#### Settimana 1 — EXTRA Input Validation (3h)

| Tempo | Argomento |
|-------|-----------|
| 09:00–09:30 | Validation vs sanitization vs encoding |
| 09:30–10:00 | Whitelist vs blacklist |
| 10:00–10:30 | Pydantic approfondito |
| 10:30–10:45 | pausa |
| 10:45–11:30 | Regex sicuro + ReDoS |
| 11:30–12:00 | bleach per HTML |

**Lab**: `M_EXTRA_input_validation_lab.py` (1.5h)

#### Settimana 2-3 — EXTRA JWT/OAuth/CSRF (4h)

| Lezione | Argomento |
|---------|-----------|
| 1 (2h) | JWT struttura + vulnerabilità (alg none, secret debole, ecc.) + OAuth 2.0 + PKCE |
| 2 (2h) | OIDC + SSO + Refresh rotation + CSRF approfondito + **Lab JWT** |

**Lab**: `M_EXTRA_jwt_lab.py`

#### Settimana 4-5 — EXTRA API Security (4h)

| Lezione | Argomento |
|---------|-----------|
| 1 (2h) | OWASP API Top 10 + BOLA + BOPLA |
| 2 (2h) | SSRF (caso Capital One) + Resource consumption + Misconfiguration + **Lab FastAPI** |

**Lab**: `M_EXTRA_api_security_lab.py`

#### Settimana 6-7 — EXTRA AI/LLM Security (4h)

| Lezione | Argomento |
|---------|-----------|
| 1 (2h) | Perché AI è diversa + OWASP LLM Top 10 + Prompt injection (direct + indirect) + RAG security |
| 2 (2h) | LLM05 output handling + LLM06 excessive agency + MITRE ATLAS + Red teaming + **Lab chatbot** |

**Lab**: `M_EXTRA_llm_chatbot_lab.py`

#### Settimana 8-9 — EXTRA Strumenti Enterprise + DevSecOps (5h)

| Lezione | Argomento |
|---------|-----------|
| 1 (2h) | SAST + SCA + DAST overview |
| 2 (3h) | Secrets scanning + Container security + SIEM + **Lab DevSecOps completo** |

**Lab**: `M_EXTRA_devsecops_lab/` (sotto-progetto completo con CI)

#### Settimana 10 — EXTRA Logging & Monitoring (2h)

| Tempo | Argomento |
|-------|-----------|
| 09:00–10:30 | A09 OWASP + structured logging + audit log immutabile + SIEM patterns |
| 10:30–11:00 | **Lab Flask logging** |

**Lab**: `M_EXTRA_logging_lab.py`

#### Settimana 11 — Lab integrato avanzato (3h)

Scenario: **estendere BancaPiccola** con:
- Login JWT + refresh rotation
- API REST con FastAPI (BOLA/BOPLA prevention)
- Chatbot LLM "supporto cliente" con difese
- Pipeline CI/CD completa

Output: report + commit pushed + workflow GitHub Actions verde.

#### Settimana 12 — Esame finale orale (2h)

Discussione individuale di 15-20 min per studente:
- Presentazione lab integrato
- 2 domande aperte su EXTRA scelti
- Critique post-mortem ("se rifacessi questo lab, cosa cambieresti?")

---

<a name="note"></a>
## 5. Note operative comuni

### 5.1 — Timing realistici

| Modulo | Timing teorico | Timing realistico (con margin) |
|--------|----------------|--------------------------------|
| M0 | 2h | 2,5h (sempre qualcuno blocca) |
| M1 | 4h | 4h ✓ |
| M2 | 6h | 6,5-7h (lab Wireshark/scapy) |
| M3 | 4h | 4h ✓ |
| M4 | 2h | 2h ✓ |
| M5 | 3h | 3,5h (workshop si allunga) |
| M6 | 9h | 9,5-10h (lab pesanti) |
| M7 | 2h | 2h ✓ ma "75 min lavoro" è ottimistico |

> **Margin del 15%** è realistico. Se hai 32h precise, taglia 5h da qualche parte.

### 5.2 — Prerequisiti per ogni lezione

Prima di ogni G:

- ✅ Slide proiettate funzionanti
- ✅ Codice di esempio testato sul tuo PC
- ✅ Materiali distribuiti (PDF/email il giorno prima)
- ✅ Compito a casa precedente verificato

### 5.3 — Quando recuperare

- **Studente che non ha fatto compito**: 5 min in pausa, non rallenti la classe.
- **Tutti hanno problemi tecnici**: dedica 20 min iniziali, salta sotto-modulo "non critico".
- **Classe avanti**: aggiungi un lab da `M_EXTRA_*`.
- **Classe indietro**: salta M6.7 (Path Traversal) o M6.6 (Supply Chain).

### 5.4 — Cosa portare a lezione

- Laptop con tutto pre-installato
- VM Linux di backup (se i lab Windows falliscono in massa)
- Penna USB con tutti i materiali (se internet aula non funziona)
- Stampe del cheat-sheet M7 per tutti (per il lab integrato)
- Cronometro per le verifiche

### 5.5 — Quando fermarsi

Se la classe è **stremata** e sta annaspando, **fermati**:
- Non finire un sotto-modulo a marce forzate.
- Chiedi una pausa di 10 min.
- Sposta il sotto-modulo alla lezione successiva.
- Meglio 90% della classe segue, che 100% del programma "fatto".

### 5.6 — Comunicazione con i discenti

Distribuisci ad inizio corso:
- README.md (mappa generale)
- README_CALENDARIO.md (questo)
- Sito o canale Telegram per Q&A asincrone
- Email del docente (orari di ricevimento)

### 5.7 — Output minimi per il discente che supera

Alla fine il discente ha:

- ✅ Cartella `cybersec-its/` con BancaPiccola + tutti i lab eseguiti
- ✅ Voto medio ≥ 60
- ✅ Report M7 consegnato
- ✅ Almeno una vulnerabilità trovata e corretta

---

> **Il calendario non è un dogma.**
> Adattalo alla classe. La cybersecurity si impara facendo, non assistendo.
