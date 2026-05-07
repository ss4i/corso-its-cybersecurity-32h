"""
🚩 APP VOLUTAMENTE VULNERABILE A SQL INJECTION

Questo file è **didattico** — gli step 1-4 del README richiedono di
sfruttare le vulnerabilità presenti in questa versione.

NON ESEGUIRE IN PRODUZIONE.
NON USARE COME RIFERIMENTO.

Vulnerabilità intenzionali:
  - Login: f-string con input utente (riga ~70)
  - Cerca: f-string con input utente nella WHERE LIKE (riga ~111)
  - Errori SQL mostrati al client (information disclosure)
  - Password in chiaro nel DB (sarà fixato in M6.4)
"""
from flask import Flask, request, render_template_string, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "lab-secret-non-usare-in-prod"

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
<p><small>Lab didattico — vedi README.md</small></p>
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

        # 🚩 VULNERABILITÀ: f-string con input utente nella query
        sql = (
            f"SELECT id, email, saldo FROM users "
            f"WHERE email = '{email}' AND password = '{pwd}'"
        )

        conn = db()
        try:
            row = conn.execute(sql).fetchone()
        except sqlite3.Error as e:
            # 🚩 INFORMATION DISCLOSURE: errore SQL al client
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
        # 🚩 VULNERABILITÀ: f-string con input utente
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
    print("⚠️  APP VULNERABILE — solo per lab didattico")
    print("    Apri http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
