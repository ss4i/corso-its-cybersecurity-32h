# Lab M6 — SQL Injection passo passo

**Modulo**: M6.2 — SQL Injection
**Tempo stimato**: 2 ore
**Livello**: principiante
**Prerequisiti**: M0 (ambiente Python+Flask), M3 (HTTP base)

> Esercizio guidato in cui costruisci tu stesso un'app **vulnerabile** a SQL Injection, la sfrutti, vedi cosa succede, poi la **correggi**. Il valore didattico è nell'**ordine** delle azioni: non ti diciamo subito la soluzione.

---

## Cosa imparerai

Al termine saprai:

1. Cos'è una SQL Injection e come si manifesta nel codice Flask
2. Eseguire un **login bypass** con `' OR '1'='1`
3. Estrarre dati arbitrari dal DB con **UNION SELECT**
4. Comprendere perché filtrare gli apici è una **pessima difesa**
5. Correggere il codice con **query parametrizzate**
6. Scrivere test automatici che verificano la difesa

---

## Setup (5 minuti)

### Crea la cartella

```bash
mkdir mini-banca-sqli
cd mini-banca-sqli
python -m venv .venv

# Attiva il venv
.\.venv\Scripts\Activate.ps1     # Windows PowerShell
source .venv/bin/activate         # macOS/Linux
```

### Installa le dipendenze

Crea `requirements.txt`:

```
flask==3.0.3
pytest==8.3.2
```

Installa:

```bash
pip install -r requirements.txt
```

### Crea il database

Crea `schema.sql`:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    saldo REAL DEFAULT 0
);

CREATE TABLE messaggi_segreti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contenuto TEXT NOT NULL
);
```

Crea `seed.py`:

```python
import sqlite3, os

if os.path.exists("banca.db"):
    os.remove("banca.db")

conn = sqlite3.connect("banca.db")
with open("schema.sql") as f:
    conn.executescript(f.read())

# Inserisci utenti (password volutamente in chiaro per il lab — vedremo M6.4)
conn.execute("INSERT INTO users (email, password, saldo) VALUES (?, ?, ?)",
             ("alice@bank.it", "alice_pass", 1500.0))
conn.execute("INSERT INTO users (email, password, saldo) VALUES (?, ?, ?)",
             ("bob@bank.it", "bob_pass", 2300.0))
conn.execute("INSERT INTO users (email, password, saldo) VALUES (?, ?, ?)",
             ("admin@bank.it", "Sup3rS3gr3t0!", 999999.0))

# Messaggi che NON dovremmo poter vedere
conn.execute("INSERT INTO messaggi_segreti (contenuto) VALUES (?)",
             ("La combinazione della cassaforte è 4815-1623",))
conn.execute("INSERT INTO messaggi_segreti (contenuto) VALUES (?)",
             ("Il piano di marketing 2027 è in /docs/strategia.pdf",))

conn.commit()
conn.close()
print("✅ DB creato. 3 utenti + 2 messaggi segreti.")
```

Esegui:

```bash
python seed.py
```

---

## Step 1 — App volutamente vulnerabile (15 minuti)

Crea `app.py`:

```python
"""
🚩 APP VOLUTAMENTE VULNERABILE
Solo per scopi didattici. NON eseguire in produzione.
"""
from flask import Flask, request, render_template_string, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "lab-secret-non-usare-in-prod"

LOGIN_PAGE = """
<!doctype html>
<title>Mini Banca</title>
<h1>🏦 Mini Banca — Login</h1>
{% if errore %}<p style="color:red">{{ errore }}</p>{% endif %}
<form method="post">
  <p>Email: <input type="text" name="email"></p>
  <p>Password: <input type="text" name="password"></p>
  <p><button type="submit">Login</button></p>
</form>
"""

DASHBOARD = """
<!doctype html>
<title>Dashboard</title>
<h1>Benvenuto, {{ user.email }}</h1>
<p>Saldo: <b>€ {{ user.saldo }}</b></p>
<p><a href="/cerca">Cerca messaggi</a> | <a href="/logout">Logout</a></p>
"""

CERCA_PAGE = """
<!doctype html>
<title>Cerca messaggi</title>
<h1>🔍 Ricerca messaggi pubblici</h1>
<form>
  <input type="text" name="q" placeholder="Cerca..." value="{{ q }}">
  <button type="submit">Cerca</button>
</form>
{% if risultati %}
<h2>Risultati:</h2>
<ul>{% for r in risultati %}<li>{{ r }}</li>{% endfor %}</ul>
{% endif %}
<p><a href="/dashboard">← torna alla dashboard</a></p>
"""


def db():
    conn = sqlite3.connect("banca.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def login():
    errore = None
    if request.method == "POST":
        email = request.form["email"]
        pwd = request.form["password"]

        # 🚩 VULNERABILITÀ: f-string con input utente nella query
        sql = f"SELECT id, email, saldo FROM users WHERE email = '{email}' AND password = '{pwd}'"

        conn = db()
        try:
            row = conn.execute(sql).fetchone()
        except sqlite3.Error as e:
            errore = f"Errore SQL: {e}"
            row = None
        conn.close()

        if row:
            session["user_id"] = row["id"]
            return redirect("/dashboard")
        else:
            errore = errore or "Email o password sbagliati"

    return render_template_string(LOGIN_PAGE, errore=errore)


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    conn = db()
    user = conn.execute("SELECT * FROM users WHERE id = ?",
                         (session["user_id"],)).fetchone()
    conn.close()
    return render_template_string(DASHBOARD, user=user)


@app.route("/cerca")
def cerca():
    if "user_id" not in session:
        return redirect("/")
    q = request.args.get("q", "")
    risultati = []
    if q:
        # 🚩 VULNERABILITÀ: ancora f-string con input utente
        sql = f"SELECT contenuto FROM messaggi_segreti WHERE contenuto LIKE '%{q}%'"
        conn = db()
        try:
            risultati = [r[0] for r in conn.execute(sql).fetchall()]
        except sqlite3.Error as e:
            risultati = [f"Errore SQL: {e}"]
        conn.close()
    return render_template_string(CERCA_PAGE, q=q, risultati=risultati)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

### Avvia l'app

```bash
python app.py
```

Apri http://127.0.0.1:5000 nel browser.

### Verifica funzionamento legittimo

1. Inserisci `alice@bank.it` / `alice_pass` → entri come Alice, vedi saldo 1500€.
2. Logout. Riprova con `alice@bank.it` / `sbagliata` → "Email o password sbagliati".

✅ Funziona. Ma c'è un buco grosso. Trovalo nel prossimo step.

---

## Step 2 — Login bypass (15 minuti)

### Esperimento

Sulla pagina di login, inserisci:

| Campo | Valore |
|-------|--------|
| Email | `alice@bank.it' --` |
| Password | `qualsiasi` |

**Premi Login.**

### Cosa succede?

Sei dentro come Alice **senza conoscere la password**.

### Capisci perché

Apri `app.py` riga 48 — la query costruita era:

```sql
SELECT id, email, saldo FROM users WHERE email = 'alice@bank.it' --' AND password = 'qualsiasi'
```

In SQL `--` è un commento. Il database ha letto:

```sql
SELECT id, email, saldo FROM users WHERE email = 'alice@bank.it'
```

→ ha trovato Alice, ti ha autenticato.

### Senza conoscere un'email valida

Inserisci:

| Campo | Valore |
|-------|--------|
| Email | `' OR '1'='1' --` |
| Password | `qualsiasi` |

La query diventa:
```sql
SELECT id, email, saldo FROM users WHERE email = '' OR '1'='1' --' AND password = ...
```

`'1'='1'` è sempre vero → ti dà il **primo utente** della tabella.

### Bypass per entrare come admin

Se sai che esiste un utente "admin", puoi:

| Campo | Valore |
|-------|--------|
| Email | `admin@bank.it' --` |
| Password | `qualsiasi` |

→ entri come admin, vedi saldo 999.999€.

### Riflessione

Senza conoscere **alcuna password**, ti sei autenticato come **qualunque utente**. È SQL Injection in versione "**login bypass**".

> Questa vulnerabilità è negli **OWASP Top 10** dal 2003 ad oggi. È **ancora la #1 vulnerabilità delle webapp** insieme a Broken Access Control. Equifax 2017, Heartland 2008, TalkTalk 2015 — tutti SQL injection.

---

## Step 3 — Estrazione dati con UNION SELECT (25 minuti)

Il login bypass è grave, ma non è il peggio. **L'attaccante può anche LEGGERE dati arbitrari dal DB**, non solo nelle tabelle a cui l'app dà accesso.

### Endpoint /cerca

Fai login con qualsiasi metodo. Poi vai su `/cerca`.

L'endpoint cerca nei messaggi pubblici. Ma è vulnerabile.

### Esperimento — vedere TUTTI i messaggi (non solo quelli che matchano)

Cerca questo:

```
%' OR '1'='1
```

→ vedi entrambi i messaggi (anche senza che la parola fosse cercata).

Funziona perché la query diventa:
```sql
SELECT contenuto FROM messaggi_segreti WHERE contenuto LIKE '%%' OR '1'='1%'
```

`'1'='1'` sempre vero → tutto restituito.

### Esperimento — UNION SELECT per leggere ALTRE tabelle

Ora la parte cattiva. Cerca:

```
xyz' UNION SELECT email FROM users --
```

→ vedi le **email di tutti gli utenti** (anche quelle che l'app non dovrebbe esporre):
- `alice@bank.it`
- `bob@bank.it`
- `admin@bank.it`

Cerca questo, e tieniti forte:

```
xyz' UNION SELECT email || ':' || password FROM users --
```

→ vedi **email + password** di tutti gli utenti, in chiaro:
- `alice@bank.it:alice_pass`
- `bob@bank.it:bob_pass`
- `admin@bank.it:Sup3rS3gr3t0!`

### Cosa è successo

`UNION` in SQL serve a unire risultati di due SELECT. L'attaccante ha:

1. Chiuso la stringa con `'`
2. Aggiunto `UNION SELECT` con i campi che voleva leggere
3. Aggiunto `--` per commentare il resto

La query finale è stata:
```sql
SELECT contenuto FROM messaggi_segreti WHERE contenuto LIKE '%xyz%'
UNION SELECT email || ':' || password FROM users --%'
```

Database ha unito i due risultati. La pagina `/cerca` mostra "messaggi pubblici"... ma in realtà sta mostrando email e password.

### Anche le tabelle del DB sistema

Cerca:

```
xyz' UNION SELECT name FROM sqlite_master WHERE type='table' --
```

→ vedi tutte le tabelle del DB:
- `users`
- `messaggi_segreti`
- `sqlite_sequence`

### Riflessione

Un endpoint che **doveva mostrare messaggi pubblici** ha permesso di **estrarre tutto il database**, password incluse. Questa è **SQL Injection a scopo di estrazione** ("**UNION-based**" nel jargon).

Combinato col login bypass, l'attacco completo è:

1. UNION SELECT → ottieni email+password
2. Login con credenziali rubate
3. Operi come utente legittimo
4. Nessun "rumore" → difficile da rilevare

---

## Step 4 — Pessime difese che NON funzionano (10 minuti)

A questo punto un programmatore ingenuo penserebbe: "filtro gli apici e sono a posto".

### Tentativo 1 — replace apici

Modifica `app.py` riga 48:

```python
email = request.form["email"].replace("'", "")
pwd = request.form["password"].replace("'", "")
sql = f"SELECT id, email, saldo FROM users WHERE email = '{email}' AND password = '{pwd}'"
```

Riavvia. Riprova `' OR '1'='1' --`. Funziona ancora male o non funziona?

✗ Sembra protetto. Ma...

### Bypass del filtro

Prova:

```
admin@bank.it" --
```

(con doppi apici invece di singoli — SQLite li accetta come delimitatori validi)

Oppure se il filtro è solo sui singoli apici, prova:

```
admin@bank.it`
```

(backtick — alcuni DB li accettano)

Oppure injection numerica (se il campo non avesse apici):

```
1 OR 1=1
```

### Bypass più sofisticati

- **Encoding**: `%27 OR %271%27=%271` (URL-encoded `'`)
- **Hex**: `\x27 OR ...`
- **Doppia escape**: `\\\' OR \\\'1\\\'=\\\'1`
- **Caratteri Unicode**: `ʼ` (modifier letter apostrophe)

> **Conclusione**: filtrare caratteri specifici è una **strategia perdente**. Gli attaccanti hanno **infiniti modi** di bypassarla. Funziona finché non arriva qualcuno bravo.

### Tentativo 2 — escape con backslash

```python
email = request.form["email"].replace("'", "\\'")
```

Bypass:
```
admin@bank.it\' --
```

L'attaccante mette già un `\` davanti all'apice. Il tuo replace fa diventare `\\\'` → SQLite interpreta `\\` come backslash literal → l'apice **resta**.

### Riflessione

> "Sanitizzo gli apici" non funziona. Mai.
> L'unica difesa robusta è **non far costruire la query dall'input**. Vediamo come.

---

## Step 5 — La correzione: query parametrizzate (15 minuti)

### Idea

Invece di **costruire la query mescolando struttura e dati**, separi:

- La **query** è costante: `"SELECT ... WHERE email = ? AND password = ?"`
- I **dati** vengono passati come parametri separati: `(email, pwd)`

Il driver del database **garantisce** che i dati non vengano interpretati come parte della struttura SQL. Indipendentemente da cosa l'utente scrive (apici, UNION, semicolons), **non viene eseguito come SQL**.

### Modifica `app.py`

Sostituisci la funzione `login` con questa versione corretta:

```python
@app.route("/", methods=["GET", "POST"])
def login():
    errore = None
    if request.method == "POST":
        email = request.form["email"]
        pwd = request.form["password"]

        # ✅ QUERY PARAMETRIZZATA — i ? sono placeholder, i dati passati separati
        sql = "SELECT id, email, saldo FROM users WHERE email = ? AND password = ?"

        conn = db()
        row = conn.execute(sql, (email, pwd)).fetchone()
        conn.close()

        if row:
            session["user_id"] = row["id"]
            return redirect("/dashboard")
        else:
            errore = "Email o password sbagliati"

    return render_template_string(LOGIN_PAGE, errore=errore)
```

### Modifica `cerca`:

```python
@app.route("/cerca")
def cerca():
    if "user_id" not in session:
        return redirect("/")
    q = request.args.get("q", "")
    risultati = []
    if q:
        # ✅ Anche qui parametrizzata
        sql = "SELECT contenuto FROM messaggi_segreti WHERE contenuto LIKE ?"
        conn = db()
        # Il pattern % lo aggiungo io ai dati, NON alla query
        risultati = [r[0] for r in conn.execute(sql, (f"%{q}%",)).fetchall()]
        conn.close()
    return render_template_string(CERCA_PAGE, q=q, risultati=risultati)
```

### Riavvia e prova gli stessi attacchi

Riavvia l'app:

```bash
python app.py
```

#### Test 1 — login bypass

Email: `' OR '1'='1' --`
Password: `qualsiasi`

→ "Email o password sbagliati" ✅ (perché ora SQLite cerca un utente con email letterale `' OR '1'='1' --` e non lo trova).

#### Test 2 — UNION SELECT

Cerca: `xyz' UNION SELECT email FROM users --`

→ nessun risultato ✅ (perché ora cerca messaggi che contengono LETTERALMENTE quella stringa).

### Cosa fa il driver dietro le quinte

Quando passi `?` nella query e dati separati, il driver SQLite:

1. **Compila** la query SQL prima (la struttura è già fissa).
2. **Manda** i dati al motore SQL come **valori già tipati** (string, int, ecc.).
3. Il motore esegue la query trattando i dati come **dati**, mai come SQL.

Non c'è "filtro" o "escape" — c'è una **separazione strutturale** che rende l'attacco **impossibile per design**.

### Ma c'è anche un altro modo: ORM

In progetti più grandi useresti **SQLAlchemy** (ORM):

```python
from sqlalchemy.orm import Session
user = session.query(User).filter_by(email=email, password=pwd).first()
```

L'ORM fa parametrizzazione **automaticamente**. Non puoi accidentalmente fare SQL injection (a meno che usi `text()` con f-string, antipattern).

---

## Step 6 — Test automatici (15 minuti)

Per essere certi che la correzione funzioni, scrivi test.

Crea `test_app.py`:

```python
"""Test automatici per verificare difesa contro SQLi."""
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_login_legittimo_funziona(client):
    """Verifica che il login normale ancora funzioni."""
    r = client.post("/", data={"email": "alice@bank.it", "password": "alice_pass"},
                     follow_redirects=False)
    # 302 redirect = login OK
    assert r.status_code == 302
    assert r.headers["Location"].endswith("/dashboard")


def test_login_password_sbagliata(client):
    r = client.post("/", data={"email": "alice@bank.it", "password": "WRONG"},
                     follow_redirects=True)
    assert b"Email o password sbagliati" in r.data


def test_sqli_login_bypass_or_1_1(client):
    """L'attacco classico ' OR '1'='1' NON deve dare login."""
    r = client.post("/", data={"email": "' OR '1'='1' --", "password": "x"},
                     follow_redirects=True)
    assert b"Email o password sbagliati" in r.data
    # NON deve essere stato fatto il login
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_sqli_login_bypass_admin_comment(client):
    """Bypass commentando la condizione password."""
    r = client.post("/", data={"email": "admin@bank.it' --", "password": "x"},
                     follow_redirects=True)
    assert b"Email o password sbagliati" in r.data
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_sqli_union_select_in_cerca(client):
    """UNION SELECT NON deve restituire dati di altre tabelle."""
    # Login prima
    client.post("/", data={"email": "alice@bank.it", "password": "alice_pass"})
    # Tenta UNION
    r = client.get("/cerca?q=xyz' UNION SELECT email FROM users --")
    # Le email NON devono apparire nei risultati
    assert b"alice@bank.it" not in r.data
    assert b"admin@bank.it" not in r.data
    assert b"bob@bank.it" not in r.data


def test_input_speciale_safe(client):
    """Caratteri speciali non rompono l'app (no 500)."""
    test_inputs = [
        "'", '"', ";", "--", "/* */", "%", "_",
        "' OR 1=1", "' UNION SELECT", "<script>alert(1)</script>",
    ]
    for inp in test_inputs:
        r = client.post("/", data={"email": inp, "password": inp},
                         follow_redirects=True)
        assert r.status_code == 200, f"Crash su input: {inp}"
```

### Esecuzione

```bash
pytest test_app.py -v
```

Output atteso:
```
test_login_legittimo_funziona PASSED
test_login_password_sbagliata PASSED
test_sqli_login_bypass_or_1_1 PASSED
test_sqli_login_bypass_admin_comment PASSED
test_sqli_union_select_in_cerca PASSED
test_input_speciale_safe PASSED
6 passed in 0.42s
```

✅ La difesa funziona ed è **verificata da test**.

> Test che impedisce regressioni in futuro: se un altro programmatore reintroduce SQLi, i test falliscono in CI.

---

## Step 7 — Difese aggiuntive (10 minuti)

Le query parametrizzate sono la **difesa primaria**. Ma in produzione si applicano anche altre difese in profondità (concetto M1):

### A. Least Privilege per l'utente DB

L'utente DB usato dalla webapp dovrebbe avere **solo i permessi necessari**:

```sql
-- ✅ Permessi minimi
GRANT SELECT, INSERT, UPDATE ON users TO webapp_user;
-- ❌ Mai dare a webapp_user
-- GRANT ALL PRIVILEGES, GRANT, DROP, CREATE, ecc.
```

Se un attaccante riuscisse comunque a fare SQLi, **non potrebbe DROPpare tabelle o leggere `pg_shadow`**.

### B. Errori generici al client

```python
try:
    row = conn.execute(sql, (email, pwd)).fetchone()
except sqlite3.Error:
    # Logga internamente, ma rispondi genericamente
    app.logger.exception("DB error during login")
    errore = "Errore interno"
```

Mai `errore = str(e)` al client — l'errore SQL rivela struttura tabelle.

### C. Rate limiting sul login

```python
# Aggiungi flask-limiter
from flask_limiter import Limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["200/hour"])

@app.route("/", methods=["GET", "POST"])
@limiter.limit("5/minute", methods=["POST"])
def login():
    ...
```

5 tentativi/minuto = brute force impossibile.

### D. Web Application Firewall (WAF)

Davanti all'app, un WAF (es. Cloudflare, ModSecurity) **filtra pattern SQLi noti** come ulteriore strato. Ma **non sostituisce** le query parametrizzate.

### E. Audit log

Logga ogni login (successo e fallimento) con email + IP. Se vedi 100 login fail consecutivi su `admin@bank.it' --`, è chiaramente un attacco.

---

## Step 8 — Recap & Checklist

### Cosa hai imparato

✅ Cos'è una SQL Injection (concatenazione di input nella query)
✅ Login bypass con `' OR '1'='1' --`
✅ Estrazione dati con `UNION SELECT`
✅ Perché filtrare gli apici NON funziona
✅ Correzione con query parametrizzate (`?` placeholder)
✅ Test automatici di regressione
✅ Difese in profondità (least priv, errori, rate limit, WAF)

### Checklist operativa SQLi (memorizzala)

```
☐ Mai f-string / + / % con input utente in query SQL
☐ Sempre placeholder ? (o %s su psycopg2) + tuple di parametri
☐ ORM (SQLAlchemy) come opzione preferita
☐ Test automatici con payload noti (' OR '1'='1', UNION, etc.)
☐ Errori generici al client, log dettagliato interno
☐ Utente DB con least privilege
☐ Rate limiting su endpoint sensibili (login, search)
☐ WAF in defense in depth (non come unica difesa)
☐ Audit log (login attempts, query sospette)
```

### Errori comuni da NON fare

| ❌ Antipattern | ✅ Pattern corretto |
|---------------|---------------------|
| `f"... WHERE id = {id}"` | `"... WHERE id = ?", (id,)` |
| `"... " + str(id)` | placeholder |
| `.replace("'", "")` | non basta, **mai** |
| Errori SQL al client | error generico + log interno |
| Webapp = DB admin | least privilege |

---

## Esercizi di approfondimento

### E1) Blind SQLi

Modifica l'app perché la pagina di login **non dica** se l'errore è "email" o "password" (entrambi → "credenziali errate"). E rimuovi il messaggio di errore SQL.

Ora l'attaccante non vede output diretto. Ma può ancora dedurre informazioni con **time-based blind**:

```
admin@bank.it' AND (SELECT CASE WHEN (...) THEN 1 ELSE randomblob(1000000000) END) --
```

Se la condizione è vera, query lentissima → attaccante deduce.

Implementa anche difesa: **timeout** sulle query.

### E2) Confronto con SQLAlchemy

Riscrivi `app.py` usando SQLAlchemy ORM al posto di sqlite3 raw. Confronta:
- Quante righe in più/meno?
- Più o meno leggibile?
- Più sicuro per default?

### E3) Test automatizzato con sqlmap

Installa sqlmap (`brew install sqlmap` o pip):

```bash
sqlmap -u "http://localhost:5000/cerca?q=test" --cookie="session=..." --batch
```

Esegui sulla **versione vulnerabile** → trova la SQLi.
Esegui sulla **versione corretta** → "no vulnerable parameters detected".

### E4) Aggiungi password hashing

Le password sono ancora in chiaro nel DB (lo vedremo in M6.4). Estendi l'app:
- Modifica `seed.py` per salvare bcrypt hash.
- Modifica `login` per `bcrypt.checkpw`.
- Aggiorna i test.

### E5) Bonus — esfiltra il DB completo

Sull'app **vulnerabile**, scrivi un piccolo script Python che, sfruttando la vulnerabilità, estrae:
- Tutte le tabelle
- Tutti i record di ogni tabella
- Tutto in un file CSV

Questo è ciò che farebbe un attaccante reale. Fai questo **solo** sulla tua app locale.

---

## Domande di verifica

1. Cos'è una "query parametrizzata"?
2. Perché `' OR '1'='1' --` permette il login bypass?
3. Cosa fa `UNION SELECT` in un attacco SQLi?
4. Perché `replace("'", "")` non protegge?
5. Quale dei 5 principi del Secure Coding viene applicato dalle query parametrizzate?
6. Una webapp gira come utente DB con permessi `ALL PRIVILEGES`. Quale principio è violato?
7. Differenza tra "in-band" e "blind" SQLi?
8. Cosa restituisce `?` come parametro in sqlite3 vs `%s` in psycopg2 (PostgreSQL)?

---

## File di questo lab

```
M6_sqli_step_by_step/
├── README.md                    ← questo file
├── requirements.txt             ← flask + pytest
├── schema.sql                   ← schema DB
├── seed.py                      ← popola DB
├── app.py                       ← APP VULNERABILE (per gli step 1-4)
├── test_app.py                  ← test automatici (step 6)
├── solution/
│   ├── app.py                   ← versione corretta (NON aprire prima!)
│   └── README.md                ← spiegazione fix
└── templates/                   ← (opzionale: template Jinja2 separati)
```

---

## Prossimo lab

**M6.3 — Broken Access Control / IDOR**

Adesso che hai imparato a difendere il login, vediamo cosa succede **dopo** l'autenticazione: l'utente loggato può accedere a dati di altri utenti?

> Spoiler: l'app che hai costruito è ancora vulnerabile. Avanti.

---

> ⚠️ **Avviso etico**
> Le tecniche imparate qui valgono **solo** sulla tua app locale e su target esplicitamente autorizzati.
> SQL injection su sistemi altrui è **reato** in Italia (Art. 615-ter c.p. — accesso abusivo + Art. 635-bis — danneggiamento informatico).
> "L'ho fatto solo per imparare" non è una difesa legale.
