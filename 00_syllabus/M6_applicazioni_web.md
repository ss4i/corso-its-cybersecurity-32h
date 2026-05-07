# M6 — Sicurezza delle Applicazioni Web (9h)

## Obiettivo

Al termine del modulo il discente sa:

1. Citare la **OWASP Top 10:2025** e collegare ogni voce a un caso reale.
2. Capire **CVE** e **CVSS**: cosa sono, come si leggono, dove si cercano.
3. **Riconoscere** in codice Python/Flask le 5 vulnerabilità più diffuse: SQLi, IDOR, Crypto Failures, XSS, Path Traversal.
4. **Sfruttarle** in laboratorio sull'app vulnerabile `bancapiccola-mini` o BancaPiccola.
5. **Correggerle** scrivendo codice difensivo e testandolo.
6. **Verificare** la propria supply chain con `pip-audit` e leggere un SBOM minimale.

## Materiale di riferimento

- `dispensa-sviluppo-sicuro-software.docx` → **Capitoli 4-10** (cuore del modulo, riusato integralmente)
- Lab pratici già pronti: `bancapiccola-mini` costruita progressivamente nei capitoli + BancaPiccola completa nel repo
- `dispensa_code_security_v8.docx` → **Capitoli 6-13** per approfondimenti opzionali (CSRF, JWT)

## Articolazione oraria

### M6.1 — OWASP Top 10 + CVE/CVSS (1h)

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:15 | **6.1.1 Cos'è OWASP**. La Top 10 nel tempo (2017 → 2021 → 2025). | Frontale |
| 0:15 – 0:35 | **6.1.2 OWASP Top 10:2025** — overview di tutte e 10 le voci, con un esempio per ognuna. | Frontale |
| 0:35 – 0:50 | **6.1.3 CVE** — formato (`CVE-YYYY-NNNNN`), database (NVD), lifecycle. Esempio: cerchiamo CVE-2024-3094. | Frontale + demo |
| 0:50 – 1:00 | **6.1.4 CVSS 3.1** — base score, vector string, bande di severity. Esempio: leggiamo il CVSS di Log4Shell. | Frontale + demo |

### M6.2 — SQL Injection (2h, lab pesante)

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:20 | **6.2.1 Ripasso SQL essenziale** — SELECT, WHERE, UNION. Cosa rendono pericolose le query "costruite con f-string". | Frontale |
| 0:20 – 0:40 | **6.2.2 Costruiamo `bancapiccola-mini`** — login vulnerabile. | **Lab guidato** |
| 0:40 – 1:00 | **6.2.3 Attacco 1: login bypass con `' OR '1'='1`**. Spieghiamo perché funziona, riga per riga. | Frontale + lab |
| 1:00 – 1:15 | **PAUSA** | |
| 1:15 – 1:40 | **6.2.4 Attacco 2: UNION SELECT**. Estrazione di dati. | **Lab guidato** |
| 1:40 – 2:00 | **6.2.5 La correzione**: query parametrizzate (`?` placeholder). Cosa fa il driver dietro le quinte. **Errore comune**: filtraggio degli apici (perché è sbagliato). Difese aggiuntive: WAF, errori generici, least privilege DB. | Frontale + lab |

### M6.3 — Broken Access Control / IDOR (1.5h)

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:15 | **6.3.1 Autenticazione vs Autorizzazione** — la confusione fondamentale. | Frontale |
| 0:15 – 0:30 | **6.3.2 Cos'è un IDOR** — esempio del numero di fattura. | Frontale |
| 0:30 – 0:55 | **6.3.3 Lab: estendiamo bancapiccola-mini con fatture**. Vediamo le fatture altrui. | **Lab guidato** |
| 0:55 – 1:15 | **6.3.4 La correzione**: ownership check server-side. Errore comune: nascondere ID nell'UI ("security by obscurity"). | Frontale + lab |
| 1:15 – 1:30 | **6.3.5 Varianti**: IDOR su PUT/DELETE/POST. Perché 403 vs 404. | Frontale |

### M6.4 — Password e crittografia (1.5h)

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:10 | **6.4.1 Encoding ≠ Hashing ≠ Encryption** — Base64 non è cifratura. Dimostrazione live. | Frontale + demo |
| 0:10 – 0:25 | **6.4.2 Perché le password si hashano**. Hash one-way, properties (preimage resistance, collision resistance). | Frontale |
| 0:25 – 0:40 | **6.4.3 Perché MD5 e SHA-1 sono morti per le password**. Velocità GPU, rainbow table. | Frontale + demo |
| 0:40 – 0:55 | **6.4.4 Salt** — cosa è, perché è obbligatorio, come si genera. | Frontale |
| 0:55 – 1:20 | **6.4.5 bcrypt** — work factor, esempio in Python. **Lab**: convertiamo bancapiccola-mini da SHA-1 a bcrypt. | **Lab guidato** |
| 1:20 – 1:30 | **6.4.6 Argon2id** — cenno: perché è "il prossimo bcrypt", quando preferirlo. | Frontale |

### M6.5 — Cross-Site Scripting (1.5h)

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:15 | **6.5.1 Come funziona un browser** + Same-Origin Policy. Perché XSS è grave. | Frontale |
| 0:15 – 0:30 | **6.5.2 I tre tipi di XSS**: Reflected, Stored, DOM-based. Esempi. | Frontale |
| 0:30 – 0:55 | **6.5.3 Lab: Reflected XSS su bancapiccola-mini**. Payload base + furto cookie con XSS. | **Lab guidato** |
| 0:55 – 1:15 | **6.5.4 Lab: Stored XSS su un commento**. La difesa: escape dell'output (Jinja2 fa già escape per default!). | **Lab guidato** |
| 1:15 – 1:30 | **6.5.5 Difese stratificate**: CSP, cookie HttpOnly, sanitizzazione input. | Frontale |

### M6.6 — Supply Chain (0.5h)

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:10 | **6.6.1 La superficie di attacco della supply chain**. CVE in dipendenze, typosquatting, dependency confusion. | Frontale |
| 0:10 – 0:25 | **6.6.2 Lab pip-audit** su bancapiccola-mini. Identifica una CVE in una versione vecchia di Flask, fixa. | **Lab guidato** |
| 0:25 – 0:30 | **6.6.3 SBOM** — cos'è, formato CycloneDX in 2 minuti. Caso XZ Utils. | Frontale |

### M6.7 — Path Traversal (1h)

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:15 | **6.7.1 Il problema**: `../etc/passwd`. Esempio in un endpoint che serve file. | Frontale |
| 0:15 – 0:40 | **6.7.2 Lab: path traversal su bancapiccola-mini**. Lettura di file fuori dalla cartella `uploads/`. | **Lab guidato** |
| 0:40 – 1:00 | **6.7.3 Le 3 difese obbligatorie**: whitelist, normalizzazione (`os.path.realpath`), validazione `startswith(BASE_DIR)`. | Frontale + lab |

## Lab del modulo (6h)

Tutti i lab sono già nella dispensa principale, capitoli 5-10. Il file `02_lab/M6_lab_index.md` (da produrre se serve) raccoglie i comandi essenziali per ognuno.

| Lab | Vulnerabilità | Tempo |
|-----|---------------|-------|
| 6.2 | SQL Injection (login bypass + UNION) | ~75 min |
| 6.3 | IDOR (lettura fatture altrui) | ~50 min |
| 6.4 | Password hashing (SHA-1 → bcrypt) | ~30 min |
| 6.5 | XSS riflessa + memorizzata | ~50 min |
| 6.6 | Supply chain (pip-audit) | ~15 min |
| 6.7 | Path traversal | ~25 min |
| **Totale lab** | | **~245 min ≈ 4h** |

(Le restanti 2h sono lezione frontale + ripasso + transizioni — totale teoria/lab combaciano col syllabus 3/6).

## Verifica

Le domande di M6 entrano nella **Verifica Finale** (V_FINALE).

Esempi:

- Quale linea di codice rende vulnerabile a SQL Injection? Riscrivila in versione sicura.
- Differenza tra `403` e `401` nelle risposte di un controllo IDOR. Perché conta?
- Perché MD5 non si usa più per le password? Cita 2 ragioni.
- Cosa fa `Jinja2` di default che protegge da XSS riflessa? Quando bisogna disattivarlo (e con cautela)?
- Cosa restituisce `pip-audit` se il `requirements.txt` ha `flask==2.0.0`?

## Errori da evitare in classe

- **Non saltare i lab "rotti"**: i lab dove l'app vulnerabile fa breach sono il momento di apprendimento più alto. Il discente deve **vedere** il proprio attacco riuscire prima di imparare la difesa.
- **Non chiudere bancapiccola-mini a fine M6**: la riprendiamo in M7 per il lab integrato.
- **Non sovraccaricare di teoria** in 9h che hanno già il loro peso. Se manca tempo: tagliare 6.6 (supply chain) prima e accennarla solo, o spostare M6.7 (path traversal) come "homework guidato".
