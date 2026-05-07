"""
App volutamente VULNERABILE per il lab DevSecOps.
NON ESEGUIRE IN PRODUZIONE.
NON USARE COME RIFERIMENTO.

Difetti intenzionali:
- Hardcoded secret (riga 14)
- SQL Injection (riga 21)
- Command Injection / RCE (riga 31)
- Debug mode in prod (riga 35)
- Bind 0.0.0.0 senza giustificazione (riga 35)
- Manca error handling
"""
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# 🚩 SECRET HARDCODED — gitleaks lo deve trovare (pattern AWS Access Key)
SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


@app.route("/login")
def login():
    user = request.args.get("user")
    pwd = request.args.get("pwd")
    conn = sqlite3.connect("db.sqlite")
    # 🚩 SQL INJECTION — Bandit lo deve trovare (B608)
    sql = f"SELECT * FROM users WHERE user='{user}' AND pwd='{pwd}'"
    return str(conn.execute(sql).fetchone())


@app.route("/run")
def run_cmd():
    cmd = request.args.get("cmd")
    import os
    # 🚩 COMMAND INJECTION / RCE — Bandit lo deve trovare (B605)
    return os.popen(cmd).read()


if __name__ == "__main__":
    # 🚩 DEBUG=True (B201) + bind 0.0.0.0 (B104)
    app.run(debug=True, host="0.0.0.0", port=5000)
