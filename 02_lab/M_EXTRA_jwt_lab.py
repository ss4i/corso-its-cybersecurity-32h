"""
Lab EXTRA — JWT + Flask con refresh token rotation

Obiettivi del lab:
1. Creare JWT con HS256 e claims standard (sub, exp, aud, iss)
2. Implementare login → access_token + refresh_token
3. Implementare /refresh con rotation
4. Implementare reuse detection (revoke famiglia)
5. Decorator @require_jwt e @require_role
6. Testare attacchi: alg none, token scaduto, reuse, audience mismatch

INSTALLAZIONE:
    pip install flask pyjwt python-dotenv

USO:
    python M_EXTRA_jwt_lab.py
    # In altro terminale: vedi sezione TEST in fondo

LIVELLO: avanzato (post M3, post EXTRA JWT/OAuth)
"""

import time
import os
import secrets
from functools import wraps
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

# === CONFIGURAZIONE ===
SECRET = os.getenv("JWT_SECRET", secrets.token_urlsafe(64))
ALGO = "HS256"
TTL_ACCESS = 15 * 60          # 15 minuti
TTL_REFRESH = 7 * 24 * 3600   # 7 giorni

# === MOCK DB UTENTI (in produzione: PostgreSQL + bcrypt) ===
USERS = {
    "alice": {"password": "alice123", "roles": ["user"]},
    "bob": {"password": "bob123", "roles": ["user"]},
    "admin": {"password": "admin123", "roles": ["user", "admin"]},
}

# === MOCK DB REFRESH TOKEN (in produzione: Redis o tabella DB) ===
# Format: {token_id: {"user": ..., "status": "ACTIVE|USED|REVOKED",
#                     "family": ..., "exp": ...}}
REFRESH_DB = {}


# === HELPER ===
def make_access_token(user: str, roles: list) -> str:
    """Crea un access token JWT con claims standard."""
    payload = {
        "sub": user,
        "roles": roles,
        "iss": "myapp",
        "aud": "myapi",
        "iat": int(time.time()),
        "exp": int(time.time()) + TTL_ACCESS,
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)


def make_refresh_token(user: str, family: str = None) -> tuple[str, str]:
    """Crea un refresh token e lo salva in 'DB'.

    Returns: (token_id, family_id)
    """
    family = family or secrets.token_urlsafe(16)
    token_id = secrets.token_urlsafe(32)
    REFRESH_DB[token_id] = {
        "user": user,
        "status": "ACTIVE",
        "family": family,
        "exp": int(time.time()) + TTL_REFRESH,
    }
    return token_id, family


def require_jwt(f):
    """Decorator: l'endpoint richiede un JWT valido."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "missing token"}), 401

        token = auth[7:]
        try:
            payload = jwt.decode(
                token, SECRET,
                algorithms=[ALGO],          # ⚠️ whitelist algoritmi
                audience="myapi",            # ⚠️ verifica audience
                issuer="myapp",              # ⚠️ verifica issuer
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token expired"}), 401
        except jwt.InvalidAudienceError:
            return jsonify({"error": "wrong audience"}), 401
        except jwt.InvalidIssuerError:
            return jsonify({"error": "wrong issuer"}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({"error": f"invalid token: {e}"}), 401

        request.user = payload
        return f(*args, **kwargs)
    return wrapper


def require_role(role: str):
    """Decorator: l'endpoint richiede uno specifico ruolo."""
    def deco(f):
        @wraps(f)
        @require_jwt
        def wrapper(*args, **kwargs):
            if role not in request.user.get("roles", []):
                return jsonify({"error": "forbidden"}), 403
            return f(*args, **kwargs)
        return wrapper
    return deco


# === ENDPOINTS ===
@app.route("/login", methods=["POST"])
def login():
    """Login: restituisce access_token + refresh_token."""
    data = request.get_json() or {}
    user = data.get("username", "")
    pwd = data.get("password", "")

    u = USERS.get(user)
    # In produzione: bcrypt.checkpw
    if not u or u["password"] != pwd:
        return jsonify({"error": "invalid credentials"}), 401

    access = make_access_token(user, u["roles"])
    refresh, family = make_refresh_token(user)

    return jsonify({
        "access_token": access,
        "refresh_token": refresh,
        "expires_in": TTL_ACCESS,
    })


@app.route("/refresh", methods=["POST"])
def refresh():
    """Refresh con rotation + reuse detection."""
    data = request.get_json() or {}
    rt = data.get("refresh_token", "")

    rec = REFRESH_DB.get(rt)
    if not rec:
        return jsonify({"error": "invalid refresh"}), 401

    # === REUSE DETECTION ===
    if rec["status"] != "ACTIVE":
        # Token già usato O revocato → REVOKE INTERA FAMIGLIA
        family = rec.get("family")
        for tid, r in REFRESH_DB.items():
            if r.get("family") == family:
                r["status"] = "REVOKED"
        app.logger.warning(
            f"REFRESH TOKEN REUSE detected for user={rec['user']} "
            f"family={family} — entire family revoked")
        return jsonify({
            "error": "token reuse detected — login again",
            "code": "REUSE"
        }), 401

    if time.time() > rec["exp"]:
        return jsonify({"error": "refresh expired"}), 401

    # === ROTATION ===
    rec["status"] = "USED"        # invalida vecchio
    user = rec["user"]
    new_access = make_access_token(user, USERS[user]["roles"])
    new_refresh, _ = make_refresh_token(user, family=rec["family"])

    return jsonify({
        "access_token": new_access,
        "refresh_token": new_refresh,
        "expires_in": TTL_ACCESS,
    })


@app.route("/logout", methods=["POST"])
def logout():
    """Logout: invalida il refresh token (e tutta la famiglia se vuoi)."""
    data = request.get_json() or {}
    rt = data.get("refresh_token", "")
    rec = REFRESH_DB.get(rt)
    if rec:
        # Revoca intera famiglia (best practice)
        family = rec.get("family")
        for tid, r in REFRESH_DB.items():
            if r.get("family") == family:
                r["status"] = "REVOKED"
    return jsonify({"status": "logged out"})


@app.route("/me")
@require_jwt
def me():
    """Endpoint protetto — chiunque autenticato."""
    return jsonify({
        "user": request.user["sub"],
        "roles": request.user["roles"],
        "exp_in_seconds": request.user["exp"] - int(time.time()),
    })


@app.route("/admin")
@require_role("admin")
def admin():
    """Endpoint protetto — solo admin."""
    return jsonify({"secret": "admin-only data"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)


# =====================================================================
# TEST DA TERMINALE (curl)
# =====================================================================
#
# 1) LOGIN
#    curl -X POST http://localhost:5000/login \
#      -H "Content-Type: application/json" \
#      -d '{"username":"alice","password":"alice123"}'
#
#    Risposta:
#    {"access_token":"eyJ...", "refresh_token":"abc...", "expires_in": 900}
#
#
# 2) ACCESSO ENDPOINT PROTETTO (sostituisci ACCESS)
#    curl http://localhost:5000/me -H "Authorization: Bearer ACCESS"
#
#    Risposta: {"user":"alice","roles":["user"],"exp_in_seconds":...}
#
#
# 3) ACCESSO ADMIN (con admin token)
#    Login come admin, poi:
#    curl http://localhost:5000/admin -H "Authorization: Bearer ACCESS_ADMIN"
#
#
# 4) REFRESH (sostituisci REFRESH)
#    curl -X POST http://localhost:5000/refresh \
#      -H "Content-Type: application/json" \
#      -d '{"refresh_token":"REFRESH"}'
#
#    Risposta: nuovo access + nuovo refresh, vecchio invalidato.
#
#
# 5) REUSE ATTACK — usa lo stesso refresh due volte
#    Prima volta: OK
#    Seconda volta: 401 + intera famiglia revocata
#      → da ora il refresh "nuovo" è anche revocato!
#
#
# 6) LOGOUT
#    curl -X POST http://localhost:5000/logout \
#      -H "Content-Type: application/json" \
#      -d '{"refresh_token":"REFRESH"}'
#
#
# =====================================================================
# ESERCIZI DI APPROFONDIMENTO
# =====================================================================
#
# E1) ALG: NONE ATTACK
#     Forgia un token con header {"alg":"none"} e payload arbitrario.
#     Mandalo a /me. Cosa succede?
#     → pyjwt rifiuta (algorithms whitelist).
#     Prova a togliere "algorithms=[ALGO]" dal decode: vedi cosa cambia.
#     Quando lo metti, è SICURO.
#
# E2) TOKEN SCADUTO
#     Riduci TTL_ACCESS a 5 secondi.
#     Logga, aspetta 6 secondi, riprova /me.
#     Errore atteso: "token expired".
#
# E3) AUDIENCE MISMATCH
#     Modifica make_access_token: cambia "aud" da "myapi" a "myotherapi".
#     Riprova /me. Errore atteso: "wrong audience".
#
# E4) ALGORITHM CONFUSION
#     Modifica decode per accettare entrambi:
#       algorithms=["HS256", "RS256"]
#     Cosa rischi? (Ricerca: algorithm confusion attack)
#
# E5) JWT IN COOKIE
#     Invece di restituire access_token in JSON, mettilo in cookie:
#         response.set_cookie("access_token", access,
#                             httponly=True, secure=True, samesite="Lax")
#     Modifica require_jwt per leggerlo dal cookie.
#     Vantaggi rispetto a localStorage?
#       → XSS non può rubarlo.
#
# E6) RATE LIMIT SU /login
#     Aggiungi flask-limiter: max 5 tentativi al minuto per IP.
#     Difesa contro brute force.
#
# =====================================================================
# DOMANDE DI VERIFICA
# =====================================================================
#
# Q1: Perché il payload JWT non è cifrato?
# Q2: Cosa fa "algorithms=['HS256']" nel decode?
# Q3: Perché il refresh token deve avere rotation?
# Q4: Cosa succede se non valido "audience"?
# Q5: Quale è la differenza tra cookie HttpOnly e localStorage per JWT?
# Q6: Quanto deve essere lungo il SECRET?
# Q7: Perché HS256 non va bene per microservizi distribuiti?
#     (Hint: chiave condivisa)
