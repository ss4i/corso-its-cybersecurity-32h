"""
App CORRETTA — versione sicura.
NON aprire prima di aver completato lo step 4 del lab.

Difese applicate:
- SECRET da env var (non in codice)
- Query parametrizzata (no SQLi)
- Endpoint /run RIMOSSO (no RCE)
- debug=False
- bind 127.0.0.1 (localhost-only)
- Error handling base
- Logging strutturato
"""
import os
import sqlite3
import logging
from flask import Flask, request, abort, jsonify

logging.basicConfig(
    level=logging.INFO,
    format='{"ts":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}',
)
log = logging.getLogger(__name__)

app = Flask(__name__)

# ✅ Secret da env var (mai in codice)
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY env var required")


@app.route("/login")
def login():
    user = request.args.get("user", "")
    pwd = request.args.get("pwd", "")
    if not user or not pwd:
        abort(400)

    try:
        conn = sqlite3.connect("db.sqlite")
        # ✅ Query parametrizzata — niente SQLi
        cursor = conn.execute(
            "SELECT id FROM users WHERE user = ? AND pwd = ?",
            (user, pwd)
        )
        row = cursor.fetchone()

        if row:
            log.info(f"login_success user={user}")
            return jsonify({"ok": True})
        else:
            log.warning(f"login_failure user={user} ip={request.remote_addr}")
            return jsonify({"ok": False}), 401
    except Exception as e:
        log.exception("login_error")
        return jsonify({"error": "internal"}), 500
    finally:
        try:
            conn.close()
        except Exception:
            pass


# ✅ Endpoint /run RIMOSSO completamente — RCE eliminata


if __name__ == "__main__":
    # ✅ debug=False, bind localhost only (dietro reverse proxy in prod)
    app.run(host="127.0.0.1", port=5000, debug=False)
