"""Test automatici — verificano che l'app sia DIFESA da SQL Injection.

Questo test va eseguito sulla versione CORRETTA (Step 5 del README).
Sulla versione vulnerabile, alcuni di questi test FALLISCONO (esattamente
ciò che vogliamo: il test diventa la "trappola" per regressioni).

Uso:
    # Prima: applica le correzioni del Step 5
    pytest test_app.py -v
"""
import os
import sqlite3
import pytest

# Setup: ricrea il DB pulito prima dei test
def setup_module(module):
    if os.path.exists("banca.db"):
        os.remove("banca.db")
    conn = sqlite3.connect("banca.db")
    with open("schema.sql") as f:
        conn.executescript(f.read())
    conn.executemany(
        "INSERT INTO users (email, password, saldo) VALUES (?, ?, ?)",
        [
            ("alice@bank.it", "alice_pass", 1500.0),
            ("bob@bank.it", "bob_pass", 2300.0),
            ("admin@bank.it", "Sup3rS3gr3t0!", 999999.0),
        ],
    )
    conn.executemany(
        "INSERT INTO messaggi_segreti (contenuto) VALUES (?)",
        [
            ("La combinazione della cassaforte è 4815-1623",),
            ("Il piano di marketing 2027 è in /docs/strategia.pdf",),
        ],
    )
    conn.commit()
    conn.close()


@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# === TEST FUNZIONALI (devono passare anche sulla versione vulnerabile) ===

def test_homepage_carica(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Mini Banca" in r.data


def test_login_legittimo_funziona(client):
    """Login con credenziali valide → 302 redirect a /dashboard."""
    r = client.post(
        "/",
        data={"email": "alice@bank.it", "password": "alice_pass"},
        follow_redirects=False,
    )
    assert r.status_code == 302
    assert r.headers["Location"].endswith("/dashboard")


def test_login_password_sbagliata(client):
    r = client.post(
        "/",
        data={"email": "alice@bank.it", "password": "WRONG"},
        follow_redirects=True,
    )
    assert b"Email o password sbagliati" in r.data


def test_login_email_inesistente(client):
    r = client.post(
        "/",
        data={"email": "nessuno@nowhere.it", "password": "x"},
        follow_redirects=True,
    )
    assert b"Email o password sbagliati" in r.data


def test_dashboard_richiede_login(client):
    """Senza login, /dashboard reindirizza a /."""
    r = client.get("/dashboard", follow_redirects=False)
    assert r.status_code == 302


# === TEST SQLI — devono FALLIRE su app vulnerabile, PASSARE su app corretta ===

def test_sqli_login_bypass_or_1_1(client):
    """L'attacco classico ' OR '1'='1' NON deve dare login."""
    r = client.post(
        "/",
        data={"email": "' OR '1'='1' --", "password": "qualsiasi"},
        follow_redirects=False,
    )
    # Non deve essere un redirect (302 = login OK)
    assert r.status_code != 302, "🚨 SQLi: login bypass riuscito con OR 1=1"


def test_sqli_login_bypass_admin_comment(client):
    """Bypass commentando la verifica password."""
    r = client.post(
        "/",
        data={"email": "admin@bank.it' --", "password": "x"},
        follow_redirects=False,
    )
    assert r.status_code != 302, "🚨 SQLi: login come admin senza password"


def test_sqli_login_bypass_unioning(client):
    """Tentativo di UNION nel login."""
    r = client.post(
        "/",
        data={
            "email": "x' UNION SELECT 1, 'fake@bank.it', 9999 --",
            "password": "x",
        },
        follow_redirects=False,
    )
    assert r.status_code != 302, "🚨 SQLi: UNION-based login bypass"


def test_sqli_union_select_in_cerca(client):
    """UNION SELECT in /cerca NON deve restituire dati di altre tabelle."""
    # Login prima
    client.post("/", data={"email": "alice@bank.it", "password": "alice_pass"})

    # Tenta UNION
    r = client.get("/cerca?q=xyz' UNION SELECT email FROM users --")

    # Le email NON devono apparire nei risultati
    assert b"alice@bank.it" not in r.data, "🚨 SQLi: UNION estratto email"
    assert b"admin@bank.it" not in r.data, "🚨 SQLi: UNION estratto email admin"


def test_sqli_password_extraction(client):
    """UNION SELECT che estrae password NON deve funzionare."""
    client.post("/", data={"email": "alice@bank.it", "password": "alice_pass"})

    r = client.get(
        "/cerca?q=xyz' UNION SELECT email || ':' || password FROM users --"
    )
    assert b"Sup3rS3gr3t0" not in r.data, "🚨 SQLi: password admin esposta"


def test_sqli_or_in_cerca(client):
    """OR '1'='1' in /cerca NON deve restituire TUTTI i messaggi."""
    client.post("/", data={"email": "alice@bank.it", "password": "alice_pass"})

    r = client.get("/cerca?q=%' OR '1'='1")

    # I messaggi segreti NON devono essere tutti restituiti via OR
    # (idealmente: nessuno se la query è parametrizzata e cerca letterale)
    assert b"cassaforte" not in r.data, "🚨 SQLi: messaggi esposti via OR"


def test_sqli_information_schema(client):
    """Tentativo di leggere sqlite_master via UNION."""
    client.post("/", data={"email": "alice@bank.it", "password": "alice_pass"})

    r = client.get(
        "/cerca?q=xyz' UNION SELECT name FROM sqlite_master WHERE type='table' --"
    )
    assert b"users" not in r.data, "🚨 SQLi: nome tabella esposto"
    assert b"messaggi_segreti" not in r.data, "🚨 SQLi: nome tabella esposto"


# === TEST INPUT GENERICI — non devono crashare ===

@pytest.mark.parametrize("inp", [
    "'", '"', ";", "--", "/* */", "%", "_",
    "' OR 1=1", "' UNION SELECT", "<script>alert(1)</script>",
    "ñ", "中文", "🔥",
    "'" * 100, "A" * 1000,
])
def test_input_speciale_no_crash(client, inp):
    """Caratteri speciali non devono causare crash 500."""
    r = client.post("/", data={"email": inp, "password": inp},
                     follow_redirects=True)
    assert r.status_code == 200, f"💥 Crash con input: {inp!r}"
