# Materiali del Corso — Indice e guida d'uso

**Cartella:** `Corso_32h/01_materiali/`
**Data:** 2026-05-06

---

## Cos'è questa cartella

Contiene **tutte le dispense didattiche** prodotte per il corso ITS Cybersecurity 32h.

I materiali sono divisi in **due gruppi**:

- **CORE (M0-M7)**: i materiali del corso 32h base. Uno per modulo. **Tutti necessari.**
- **EXTRA (M_EXTRA_*)**: materiali integrativi che colmano lacune del corso base. **Opzionali nel 32h, fondamentali per un Modulo Avanzato di II anno.**

---

## File CORE (M0-M7) — corso 32h base

| File | Modulo | Ore | Note |
|------|--------|-----|------|
| `M0_setup_ambiente.md` | M0 — Setup ambiente | 2h | Installazioni guidate + troubleshooting per il docente |
| `M1_fondamenti_cybersecurity.md` | M1 — Fondamenti | 4h | CIA, tassonomia minacce, 5 casi reali, 5 principi |
| `M2_networking_isoosi.md` | M2 — Networking & ISO/OSI | 6h | Stack completo, Wireshark, lab Python (più corposo) |
| `M3_http.md` | M3 — Protocollo HTTP | 4h | Estende dispensa HTTP base con focus security |
| `M4_normativa.md` | M4 — Normativa | 2h | GDPR/NIS2/CRA + 5 casi italiani + quiz |
| `M5_security_privacy_by_design.md` | M5 — Security & Privacy by Design | 3h | STRIDE, Cavoukian, DPIA, workshop su BancaPiccola |
| `M6_applicazioni_web.md` | M6 — Applicazioni Web | 9h | Orchestratore Cap 4-10 + checklist + cheat-sheet payload |
| `M7_lab_integrato.md` | M7 — Lab Integrato | 2h | Briefing, cheat-sheet, valutazione, ground truth docente |

> **Totale ore CORE: 32h**, come previsto.

---

## File EXTRA — moduli integrativi

| File | Argomento | Ore | Quando usarlo |
|------|-----------|-----|---------------|
| `M_EXTRA_jwt_oauth_csrf.md` | JWT, OAuth 2.0, OIDC, SSO, CSRF approfondito | 3-4h | Lettura tra G6-G7 o lab opzionale in M3 |
| `M_EXTRA_api_security.md` | OWASP API Security Top 10 (BOLA, BOPLA, SSRF...) | 3h | Dopo M6 o II anno |
| `M_EXTRA_input_validation.md` | Pydantic, regex, sanitization (bleach), JSON Schema | 2-3h | **Da inserire prima di M6.2** |
| `M_EXTRA_strumenti_enterprise.md` | SAST/DAST/SCA/SIEM, CI/CD security, Bandit, Snyk, Trivy | 4-5h | "Primo giorno in azienda" — lettura assegnata |
| `M_EXTRA_ai_llm_security.md` | OWASP LLM Top 10, prompt injection, MITRE ATLAS, RAG security | 4h | **OBBLIGATORIO per ogni corso 2026+** |
| `M_EXTRA_logging_monitoring.md` | OWASP A09, structured logging, audit log, SIEM, SOC | 2h | Dopo M6.6 (supply chain) |

> **Totale ore EXTRA**: ~18-21h. Sufficienti a costruire un **secondo corso di 32h "Avanzato"** o a estendere il primo corso a 50h.

---

## Suggerimenti d'uso

### Per il corso 32h base (esecuzione standard)

Usa **solo CORE**. Gli EXTRA sono distrazione.

Eccezione: distribuisci `M_EXTRA_strumenti_enterprise.md` come **lettura post-corso** ("cosa troverai in azienda"). Aiuta lo studente all'inserimento lavorativo.

### Per un corso 32h "moderno 2026" (raccomandato)

Modifica così la programmazione:

| Modulo | Ore originali | Ore raccomandate | Modifica |
|--------|---------------|-------------------|----------|
| M0 | 2 | 2 | invariato |
| M1 | 4 | 3 | togli 1h dai casi reali (rivedibili come homework) |
| M2 | 6 | 5 | togli 1h, sposta sub-modulo "vulnerabilità protocollo" come homework |
| M3 | 4 | 4 | invariato — ma assegna `M_EXTRA_jwt_oauth_csrf` come pre-lettura |
| M4 | 2 | 2 | invariato |
| M5 | 3 | 3 | invariato |
| M6 | 9 | 9 | aggiungi M6.0 "Input Validation" da `M_EXTRA_input_validation` (1h, togli 1h da SQLi) |
| M7 | 2 | 2 | invariato |
| **+M8 NUOVO** | — | **2h** | AI/LLM Security base (cap 1-3 di `M_EXTRA_ai_llm_security`) |
| **Totale** | **32** | **32** | bilanciato |

> Risultato: corso 32h che copre anche i fondamentali AI/LLM e input validation, scoperti dal corso originale.

### Per un corso 64h (32h base + 32h avanzato)

- **32h base**: tutti i CORE.
- **32h avanzato**:
  - JWT/OAuth/CSRF approfondito (4h)
  - API Security (4h)
  - Input Validation deep (3h)
  - Strumenti Enterprise (DevSecOps) (5h)
  - AI/LLM Security completo (6h)
  - Logging & Monitoring + intro SOC (4h)
  - Lab integrato avanzato (BancaPiccola → API + JWT + LLM chatbot) (4h)
  - Verifica finale avanzata (2h)

### Per un singolo modulo monografico (mezza giornata)

Ogni file EXTRA è autonomo e può essere usato come materiale di un modulo di 3-4h (es. webinar professionale, masterclass).

---

## Convenzioni

- **Formato**: Markdown CommonMark + tabelle GFM
- **Lingua**: italiano
- **Esempi codice**: principalmente Python (Flask/FastAPI), occasionalmente bash
- **Cheat-sheet**: payload reali per uso didattico (sempre con avviso legale)
- **Riferimenti**: link a OWASP, NIST, MITRE, OWASP, vendor docs

## Conversione in altri formati

```bash
# Tutti i materiali → docx
cd Corso_32h/01_materiali
for f in *.md; do
  pandoc "$f" -o "../docx/01_materiali/${f%.md}.docx" --toc --toc-depth=2 \
    -V geometry:margin=2cm
done

# Materiale singolo → PDF (richiede LaTeX)
pandoc M2_networking_isoosi.md -o M2_networking_isoosi.pdf --toc -V geometry:margin=2cm

# Slide PowerPoint → vedi 04_slide/
```

## Manutenzione

| Frequenza | Cosa rivedere |
|-----------|----------------|
| **Annuale** | OWASP Top 10 (versione corrente) |
| **Annuale** | OWASP LLM Top 10 (cambia ogni anno) |
| **Trimestrale** | CVE citate (es. CVE-2024-3094 sarà obsoleta nel 2027) |
| **Annuale** | Casi italiani (ne escono nuovi dal Garante) |
| **Quando cambiano** | NIS 2 transposition, CRA secondary acts |
| **Annuale** | Tool list (sempre nuovi DAST/SAST) |

---

## Per il docente — flusso d'uso

### Prima del corso

1. Leggi `00_syllabus/00_README.md` per la struttura ore.
2. Leggi i syllabus M0-M7 in `00_syllabus/M*.md`.
3. Leggi i materiali CORE in `01_materiali/M*.md`.
4. Decidi se aggiungere materiale EXTRA (e quale).
5. Testa i lab (Wireshark, Python, Flask) sull'aula reale.
6. Verifica disponibilità di **BancaPiccola-vuln** e **BancaPiccola-secure**.
7. Stampa il "ground truth" di M7 cap 5 per te.

### Durante il corso

1. Segui i syllabus per il timing.
2. I materiali CORE sono la "dispensa dello studente".
3. Usa le slide in `04_slide/M*.pptx` per la proiezione.
4. Distribuisci i template lab da `02_lab/`.
5. Somministra V1 a fine M3, V2 a fine M5, V_FINALE a fine corso.
6. Valuta lab M7 con la griglia in `00_syllabus/M7_lab_integrato.md`.

### Dopo il corso

1. Distribuisci EXTRA come letture per chi vuole approfondire.
2. Raccogli feedback discenti per migliorare la prossima edizione.
3. Aggiorna CVE/casi se >6 mesi.

---

> **Crediti**: Ing. Alessandro Manneschi · ITS Prodigi · ITS Empoli · SS4I · 2026
