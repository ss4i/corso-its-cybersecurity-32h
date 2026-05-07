"""
✅ APP CORRETTA — versione sicura.

NON aprire questo file prima di aver completato gli Step 1-4 del README.

Difese applicate:
  - Login: query parametrizzata con ? placeholder (no SQLi)
  - Cerca: stessa cosa, anche per LIKE
  - Errori generici al client + log interno (no information disclosure)
  - dashboard non cambia (era già parametrizzata)

Le password sono ancora in chiaro per coerenza con il lab. Il fix di
hashing si vede nel modulo M6.4.
"""
import logging
from flask import Flask, request, render_template_string, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "lab-secret-non-usare-in-prod"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

LOGIN_PAGE = """
<!doctype html>
<html lang="it">
<head><meta charset="utf-8"><title>Mini Banca — Login</title></head>
<body style="font-family: sans-serif; max-width: 500px; margin: 50px auto;">
<h1>🏦 Mini Banca — Login</h1>
{% if errore %}<p style="color:red"><b>{{ errore }}</b></p>{% endif %}
<form method="post">
  <p>Email: <input type="text" name="email" required style="width:100%"></p>
  <p>Password: <input type="text" name="password" required style="width:100%"></p>
  <p><button type="submit">Login</button></p>
</form>
<hr>
<p><small>Lab didattico — versione SECURE</small></p>
</body></html>
"""

DASHBOARD = """
<!doctype html>
<html lang="it">
<head><meta charset="utf-8"><title>Dashboard</title></head>
<body style="font-family: sans-serif; max-width: 500px; margin: 50px auto;">
<h1>Benvenuto, {{ user["email"] }}</h1>
<p>Saldo: <b>€ {{ "%.2f"|format(user["saldo"]) }}</b></p>
<p>
  <a href="/cerca">🔍 Cerca messaggi</a> |
  <a href="/logout">Logout</a>
</p>
</body></html>
"""

CERCA_PAGE = """
<!doctype html>
<html lang="it">
<head><meta charset="utf-8"><title>Cerca messaggi</title></head>
<body style="font-family: sans-serif; max-width: 700px; margin: 50px auto;">
<h1>🔍 Cerca messaggi pubblici</h1>
<form>
  <input type="text" name="q" placeholder="Cerca..." value="{{ q }}" style="width:60%">
  <button type="submit">Cerca</button>
</form>
{% if risultati %}
<h2>Risultati ({{ risultati|length }}):</h2>
<ul>{% for r in risultati %}<li>{{ r }}</li>{% endfor %}</ul>
{% elif q %}
<p><i>Nessun risultato per: {{ q }}</i></p>
{% endif %}
<p><a href="/dashboard">← torna alla dashboard</a></p>
</body></html>
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

        # ✅ QUERY PARAMETRIZZATA — placeholder ?, dati separati
        sql = "SELECT id, email, saldo FROM users WHERE email = ? AND password = ?"

        conn = db()
        try:
            row = conn.execute(sql, (email, pwd)).fetchone()
        except sqlite3.Error:
            # ✅ Errore generico al client, dettaglio nei log interni
            log.exception("Errore DB durante login")
            errore = "Errore interno del server"
            row = None
        finally:
            conn.close()

        if row:
            session["user_id"] = row["id"]
            log.info(f"login_success email={email}")
            return redirect("/dashboard")
        else:
            log.warning(f"login_failure email={email[:50]}")
            errore = errore or "Email o password sbagliati"

    return render_template_string(LOGIN_PAGE, errore=errore)


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    conn = db()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (session["user_id"],)
    ).fetchone()
    conn.close()
    if user is None:
        return redirect("/logout")
    return render_template_string(DASHBOARD, user=user)


@app.route("/cerca")
def cerca():
    if "user_id" not in session:
        return redirect("/")

    q = request.args.get("q", "")
    risultati = []

    if q:
        # ✅ QUERY PARAMETRIZZATA per LIKE — il pattern % lo aggiungiamo ai dati,
        #    NON alla query string
        sql = "SELECT contenuto FROM messaggi_segreti WHERE contenuto LIKE ?"
        conn = db()
        try:
            risultati = [
                r[0] for r in conn.execute(sql, (f"%{q}%",)).fetchall()
            ]
        except sqlite3.Error:
            log.exception("Errore DB durante ricerca")
            risultati = []
        finally:
            conn.close()

    return render_template_string(CERCA_PAGE, q=q, risultati=risultati)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    print("✅ APP SECURE — versione corretta")
    print("    Apri http://127.0.0.1:5000")
    app.run(debug=False, port=5000)
