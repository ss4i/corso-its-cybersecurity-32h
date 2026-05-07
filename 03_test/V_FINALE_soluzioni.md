# Verifica Finale — SOLUZIONI

**Punteggio totale:** 100
**Soglia di sufficienza:** 60

---

## Sezione A — Scelta multipla (15 × 2 = 30)

| # | Risposta | Note |
|---|----------|------|
| A1 | **b** | Manca salt + SHA-1 debole |
| A2 | **c** | IDOR = cambio ID per accedere a risorse altrui |
| A3 | **b** | XSS Stored (in campo commento, persiste) |
| A4 | **b** | f-string + variabile in SQL = SQLi |
| A5 | **b** | `bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())` |
| A6 | **c** | `pip-audit` |
| A7 | **a** | `../` → uscita dalla directory |
| A8 | **b** | 403 Forbidden |
| A9 | **a** | SameSite Strict/Lax |
| A10 | **b** | `\|safe` disabilita escape Jinja2 |
| A11 | **c** | Supply Chain |
| A12 | **c** | bcrypt o Argon2id |
| A13 | **b** | Rischio elevato (Art. 35 GDPR) |
| A14 | **b** | Forza HTTPS dopo prima visita |
| A15 | **d** | Disabilitare header di sicurezza è l'opposto di una mitigazione |

---

## Sezione B — Risposta breve (5 × 4 = 20)

### B1. Tre vulnerabilità OWASP Top 10:2025

Esempio di risposta corretta (3 tra le seguenti):

| Vulnerabilità | Scenario |
|---------------|----------|
| A01 Broken Access Control | IDOR su `/fattura/<id>` per leggere fatture altrui |
| A02 Cryptographic Failures | Password salvate in MD5 senza salt |
| A03 Injection | Form di login con SQL Injection |
| A04 Insecure Design | API che restituisce sempre tutti i campi utente, anche password hash |
| A06 Vulnerable Components | Flask 2.0.0 con CVE nota |

### B2. Perché MD5 è inadeguato

- **Velocità**: GPU calcolano miliardi di MD5/secondo → brute force banale.
- **Collisioni note**: chiunque può generare 2 input con stesso MD5.
- **Rainbow tables**: tabelle pre-calcolate per password comuni.
- **No salt**: stessa password → stesso hash → enumerabile.

**Alternativa**: **bcrypt** (work factor configurabile, salt automatico) o **Argon2id** (più moderno, vincitore PHC, resistenza a GPU + ASIC). bcrypt è la scelta più matura/diffusa, Argon2id è preferibile per nuove app.

### B3. Risposta uniforme 401

Risposta uniforme per "utente non esiste" e "password sbagliata" evita la **user enumeration**: un attaccante non può sapere quali email sono registrate. Risposte diverse permettono di compilare liste di email valide e poi fare brute force mirato.

> 4 pt: 2 per concetto + 2 per termine "user enumeration" o equivalente.

### B4. Authentication vs Authorization

| Differenza | Authentication | Authorization |
|------------|---------------|---------------|
| Domanda | "Chi sei?" | "Cosa puoi fare?" |
| Tempo | All'inizio (login) | A ogni richiesta |
| Esempio | Inserisci email+pwd | Verifica che `user_id == fattura.owner_id` |

> 1.3 pt per ogni differenza con esempio.

### B5. Stack trace su /api/cerca

- **STRIDE**: **I — Information Disclosure** (dettagli interni dell'app esposti).
- **Principio violato**: **Fail Secure** (in caso di errore, non dovrebbe rivelare info interne) e/o **Defense in Depth**.
- **Correzione**: error handler globale che logga l'eccezione internamente e restituisce risposta generica `{"error": "Internal server error"}` con HTTP 500. In produzione `app.config["DEBUG"] = False`.

> 1 pt STRIDE + 1 pt principio + 2 pt correzione.

---

## Sezione C — Code review (3 × 10 = 30)

### C1. Login vulnerabile

**Vulnerabilità identificate** (3 di queste, 2 pt):

1. **SQL Injection** nel costrutto f-string.
2. **SHA-1 senza salt** per password (Cryptographic Failures).
3. **No rate limiting** (brute force possibile).
4. **Risposta uniforme buona ma...** non c'è log di tentativi falliti (Repudiation).
5. **No protezione contro user enumeration via timing**.

**Payload bypass** (2 pt):
```
email = anything' OR '1'='1' --
```
La query diventa: `SELECT id, password FROM users WHERE email = 'anything' OR '1'='1' --'`. La condizione è sempre vera, e il controllo bcrypt potrebbe fallire — ma se l'attaccante lo combina con UNION SELECT, può inserire un hash che conosce.

**Versione corretta** (6 pt):

```python
import bcrypt
from flask import request, session, redirect
from sqlalchemy import select

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip().lower()
    pwd = request.form.get("password", "")

    # Validazione email basica
    if not email or "@" not in email or len(email) > 254:
        return "Email non valida", 400

    # Query parametrizzata (SQLAlchemy ORM)
    user = User.query.filter_by(email=email).first()

    # Risposta UNIFORME per non-esistenza e password sbagliata
    if user is None or not bcrypt.checkpw(
            pwd.encode("utf-8"), user.password_hash):
        # log di sicurezza interno
        app.logger.warning(f"Failed login for {email}")
        return "Email o password errati", 401

    session["user_id"] = user.id
    session.permanent = True
    return redirect("/dashboard")
```

### C2. IDOR

**Vulnerabilità** (3 pt):
> Manca completamente il controllo di **autorizzazione**. `Fattura.query.get(fid)` restituisce qualsiasi fattura senza verificare che l'utente loggato sia il proprietario. Inoltre manca il controllo di autenticazione (utente loggato).

**Status code corretto** (2 pt): **403 Forbidden** (autenticato ma non autorizzato). 404 sarebbe sbagliato (rivela esistenza/non-esistenza).

**Versione corretta** (5 pt):

```python
from flask import abort, session
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            abort(401)  # 401 perché non autenticato
        return f(*args, **kwargs)
    return wrapper

@app.route("/fattura/<int:fid>")
@login_required
def fattura(fid):
    f = Fattura.query.get(fid)
    if f is None:
        abort(404)
    if f.owner_id != session["user_id"]:
        abort(403)  # 403: ownership check fallito
    return render_template("fattura.html", fattura=f)
```

### C3. Path Traversal

**Vulnerabilità** (2 pt):
> **Path Traversal** (CWE-22). OWASP: A01 Broken Access Control. L'attaccante può fornire `file=../../etc/passwd` e leggere file fuori dalla cartella `uploads/`.

**2 payload** (2 pt):
- `../../etc/passwd` (Linux)
- `..\..\Windows\System32\drivers\etc\hosts` (Windows)
- `../app.py` (codice sorgente)
- `....//....//etc/passwd` (encoding bypass su filtri ingenui)

**Versione corretta** (6 pt):

```python
import os
from flask import abort, send_from_directory

UPLOAD_DIR = os.path.realpath("./uploads")
ALLOWED_EXTS = {".pdf", ".png", ".jpg", ".jpeg"}

@app.route("/download")
@login_required
def download():
    filename = request.args.get("file", "")

    # 1) Validazione: solo nome file, niente path
    if not filename or "/" in filename or "\\" in filename or filename.startswith("."):
        abort(400)

    # 2) Validazione estensione (whitelist)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTS:
        abort(400)

    # 3) Risoluzione path completo + check che sia dentro UPLOAD_DIR
    full_path = os.path.realpath(os.path.join(UPLOAD_DIR, filename))
    if not full_path.startswith(UPLOAD_DIR + os.sep):
        abort(403)

    # 4) Esistenza
    if not os.path.isfile(full_path):
        abort(404)

    # 5) Servizio sicuro
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)
```

> Punteggio: 1 pt per ogni controllo (validazione path, whitelist ext, realpath, startswith, esistenza, send_from_directory).

---

## Sezione D — Scenario integrato MyDocs (20)

### D1. Vulnerabilità identificate (8 pt)

5 problemi tra (1.6 pt ciascuno):

| # | Problema | Categoria |
|---|----------|-----------|
| 1 | Password in MD5 | A02 Cryptographic Failures |
| 2 | App gira come root | Least Privilege violato |
| 3 | Certificato HTTPS scaduto | A02 Cryptographic Failures + Defense in Depth |
| 4 | No MFA | A07 Identification and Authentication Failures |
| 5 | Cookie sessione senza Secure/HttpOnly/SameSite | A05 Security Misconfiguration |
| 6 | Backup S3 in bucket pubblico | A05 Security Misconfiguration + Information Disclosure |
| 7 | Link `/doc/<uuid>` se prevedibile/non revocabile → IDOR | A01 Broken Access Control |
| 8 | Filesystem locale per docs (no cifratura, single point of failure) | A04 Insecure Design |
| 9 | Upload PDF senza scansione/validazione | A04 Insecure Design / A03 Injection (PDF malevoli) |

### D2. Severity (4 pt)

Esempio di assegnazione (0.8 pt per ognuna):

| # | Severity | Giustificazione |
|---|----------|------------------|
| Backup S3 pubblico | **Critical** | Esfiltrazione completa DB + documenti studi legali |
| Password MD5 | **High** | Compromissione massiva di account in caso di dump DB |
| App come root | **High** | Una sola RCE diventa compromissione totale del server |
| Certificato HTTPS scaduto | **Medium** | Browser warning + possibile MITM |
| No MFA | **Medium** | Account takeover più facile |
| Cookie senza attributi sicurezza | **Medium** | Furto sessione via XSS o sniffing |

### D3. Soluzioni 2 problemi più critici (4 pt)

Esempi:

**Problema 1 — Backup S3 pubblico**:
**Soluzione**: rimuovere immediatamente accesso pubblico al bucket; impostare ACL `private`; abilitare cifratura SSE-S3 (o KMS); verificare con `aws s3api get-bucket-policy`; rotazione delle credenziali esposte.

**Problema 2 — Password in MD5**:
**Soluzione**: migrazione a bcrypt al primo login successivo dell'utente (rehash on login); imporre cambio password con notifica; invalidare tutte le sessioni; audit dei log accessi del periodo a rischio.

### D4. Norme violate (4 pt)

**GDPR Art. 32** — Sicurezza del trattamento. Violato perché:
- Password in MD5 = **non** "misura tecnica adeguata" per password.
- Backup pubblico = **mancata** protezione dei dati a riposo.
- Cookie senza Secure = **mancata** cifratura in transito.

**NIS 2 Art. 21 + Allegato I** — Misure di gestione dei rischi cyber. Se MyDocs serve studi legali su larga scala, potrebbe ricadere in "soggetto importante" del settore "Servizi digitali". Violato perché:
- Mancano misure di base (MFA, cifratura, gestione vulnerabilità).
- Mancanza di processi di notifica incidenti (Art. 23).

> 2 pt GDPR + 2 pt NIS 2 con riferimento corretto.

---

## Griglia di valutazione

| Voto | Range punti |
|------|-------------|
| Lode/Eccellente | 95-100 |
| Eccellente | 85-94 |
| Buono | 75-84 |
| Discreto | 65-74 |
| Sufficiente | 60-64 |
| Insufficiente | < 60 (recupero) |

> **Voto finale del corso** = 35% Verifica finale + 25% V1 + 20% V2 + 20% Lab integrato M7.
