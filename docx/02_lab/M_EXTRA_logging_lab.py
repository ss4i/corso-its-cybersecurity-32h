"""
Lab EXTRA — Flask Logging Strutturato + Audit Log + Detection

Obiettivi del lab:
1. Logging strutturato JSON (Elastic Common Schema)
2. Middleware before/after request con timing
3. Decorator @audit_action per azioni critiche
4. Detection inline brute force
5. Audit log con hash chain (immutabile)
6. SIEM-ready output

INSTALLAZIONE:
    pip install flask python-json-logger

USO:
    python M_EXTRA_logging_lab.py
    # vedi TEST in fondo

LIVELLO: intermedio
"""

import logging
import time
import hashlib
import json
import secrets
from collections import defaultdict
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, g
from pythonjsonlogger import jsonlogger


# =====================================================================
# 1. SETUP LOGGING STRUTTURATO (ECS-style)
# =====================================================================
def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"asctime": "@timestamp", "levelname": "level",
                       "name": "logger", "message": "msg"},
    ))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]


setup_logging()
app_log = logging.getLogger("app")
audit_log = logging.getLogger("audit")
security_log = logging.getLogger("security")


# =====================================================================
# 2. AUDIT LOG IMMUTABILE CON HASH CHAIN
# =====================================================================
audit_chain = []   # in produzione: DB con solo INSERT permesso
last_hash = "0" * 64


def append_audit(actor: dict, action: str, resource: dict,
                 outcome: str, context: dict = None) -> str:
    """Append a un audit log immutabile.

    Hash chain: self_hash = SHA256(prev_hash + entry_json)
    Se qualcuno modifica un'entry, gli hash successivi non quadrano.
    """
    global last_hash
    entry = {
        "audit_id": secrets.token_hex(16),
        "ts": datetime.utcnow().isoformat() + "Z",
        "actor": actor,
        "action": action,
        "resource": resource,
        "outcome": outcome,
        "context": context or {},
        "prev_hash": last_hash,
    }
    canonical = json.dumps(entry, sort_keys=True)
    self_hash = hashlib.sha256((last_hash + canonical).encode()).hexdigest()
    entry["self_hash"] = self_hash
    audit_chain.append(entry)
    last_hash = self_hash

    # Logga anche nel logger
    audit_log.info("audit_event", extra={"audit_entry": entry})
    return self_hash


def verify_audit_chain() -> bool:
    """Ricalcola tutti gli hash. Se uno non quadra → tampering."""
    prev = "0" * 64
    for entry in audit_chain:
        original_self_hash = entry.get("self_hash")
        # Ricostruisce senza self_hash
        clone = {k: v for k, v in entry.items() if k != "self_hash"}
        clone["prev_hash"] = prev
        canonical = json.dumps(clone, sort_keys=True)
        recalc = hashlib.sha256((prev + canonical).encode()).hexdigest()

        if recalc != original_self_hash:
            return False
        prev = original_self_hash
    return True


# =====================================================================
# 3. DETECTION INLINE — Brute Force
# =====================================================================
failed_logins = defaultdict(list)   # ip → [timestamp, ...]
ALERT_THRESHOLD = 5
ALERT_WINDOW = 60       # secondi


def record_failed_login(ip: str, user: str):
    now = datetime.utcnow()
    failed_logins[ip] = [t for t in failed_logins[ip]
                          if now - t < timedelta(seconds=ALERT_WINDOW)]
    failed_logins[ip].append(now)

    if len(failed_logins[ip]) >= ALERT_THRESHOLD:
        security_log.error("brute_force_alert", extra={
            "event": {"action": "security.brute_force_detected",
                      "category": ["intrusion_detection"], "outcome": "alert",
                      "severity": "high"},
            "source": {"ip": ip},
            "user": {"name": user},
            "count": len(failed_logins[ip]),
            "window_seconds": ALERT_WINDOW,
        })
        # In produzione: blocca IP, notifica SOC


# =====================================================================
# 4. FLASK APP
# =====================================================================
app = Flask(__name__)


# === Middleware: log every request ===
@app.before_request
def before():
    g.start = time.time()
    g.correlation_id = request.headers.get("X-Correlation-ID",
                                            secrets.token_hex(8))


@app.after_request
def after(response):
    elapsed_ms = (time.time() - g.start) * 1000
    app_log.info("http_request", extra={
        "event": {"action": "http.request",
                  "category": ["web"],
                  "outcome": "success" if response.status_code < 400 else "failure"},
        "http": {
            "request": {"method": request.method, "url": request.url},
            "response": {"status_code": response.status_code,
                         "bytes": response.content_length},
        },
        "source": {"ip": request.remote_addr,
                   "user_agent": {"original": request.user_agent.string}},
        "duration_ms": round(elapsed_ms, 2),
        "correlation_id": g.correlation_id,
    })
    return response


# === Decorator: audit per azioni critiche ===
def audit_action(action: str):
    """Decora un endpoint per loggare in audit log."""
    def deco(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = request.headers.get("X-User-Id", "anonymous")
            outcome = "unknown"
            try:
                result = f(*args, **kwargs)
                outcome = "success"
                return result
            except Exception as e:
                outcome = "failure"
                raise
            finally:
                append_audit(
                    actor={"type": "user", "id": user_id,
                           "ip": request.remote_addr},
                    action=action,
                    resource={"type": request.endpoint,
                              "url": request.url},
                    outcome=outcome,
                )
        return wrapper
    return deco


# === Mock DB ===
USERS = {1: {"name": "Alice", "role": "user"},
         2: {"name": "Bob", "role": "user"},
         3: {"name": "Admin", "role": "admin"}}


# === Endpoints ===
@app.post("/login")
def login():
    data = request.get_json() or {}
    user = data.get("user", "")
    pwd = data.get("pwd", "")

    # Simulazione (in produzione: bcrypt)
    if user == "alice" and pwd == "alice123":
        app_log.info("login_success", extra={
            "event": {"action": "auth.login.success",
                      "category": ["authentication"],
                      "outcome": "success"},
            "user": {"name": user},
            "source": {"ip": request.remote_addr},
        })
        # Audit
        append_audit(
            actor={"type": "user", "name": user, "ip": request.remote_addr},
            action="auth.login",
            resource={"type": "session"},
            outcome="success",
        )
        return jsonify({"token": "fake-token-xyz"})
    else:
        # Log + detection
        app_log.warning("login_failure", extra={
            "event": {"action": "auth.login.failure",
                      "category": ["authentication"],
                      "outcome": "failure", "reason": "invalid_credentials"},
            "user": {"name": user},
            "source": {"ip": request.remote_addr},
        })
        record_failed_login(request.remote_addr, user)
        return jsonify({"error": "invalid"}), 401


@app.delete("/users/<int:uid>")
@audit_action("user.delete")
def delete_user(uid):
    if uid not in USERS:
        return jsonify({"error": "not found"}), 404
    deleted = USERS.pop(uid)
    return jsonify({"deleted_user_id": uid, "deleted_user_name": deleted["name"]})


@app.put("/users/<int:uid>/role")
@audit_action("user.role_changed")
def change_role(uid):
    """Cambio ruolo — azione critica per audit."""
    if uid not in USERS:
        return jsonify({"error": "not found"}), 404
    new_role = (request.json or {}).get("role")
    if new_role not in ("user", "admin"):
        return jsonify({"error": "invalid role"}), 400

    old_role = USERS[uid]["role"]
    USERS[uid]["role"] = new_role

    # Log dedicato per privilege escalation detection
    if new_role == "admin" and old_role != "admin":
        security_log.warning("privilege_escalation", extra={
            "event": {"action": "authz.role_changed",
                      "category": ["iam"],
                      "outcome": "success", "severity": "high"},
            "user": {"id": uid, "old_role": old_role, "new_role": new_role},
        })

    return jsonify({"user_id": uid, "old_role": old_role, "new_role": new_role})


@app.get("/users")
def list_users():
    return jsonify(list(USERS.values()))


@app.get("/audit/verify")
def verify_chain():
    """Verifica integrità audit chain."""
    valid = verify_audit_chain()
    return jsonify({"valid": valid, "entries": len(audit_chain)})


@app.errorhandler(Exception)
def handle_error(e):
    app_log.exception("unhandled_exception", extra={
        "event": {"action": "error.unhandled",
                  "category": ["error"], "outcome": "failure"},
    })
    return jsonify({"error": "internal"}), 500


# =====================================================================
# DEMO standalone (senza Flask)
# =====================================================================
def demo():
    """Esegue una sequenza di azioni e mostra logging."""
    print("=" * 70)
    print("DEMO LOGGING + AUDIT")
    print("=" * 70)

    # Simula azioni
    append_audit(
        actor={"type": "user", "id": "alice", "ip": "1.2.3.4"},
        action="auth.login",
        resource={"type": "session"},
        outcome="success",
    )
    append_audit(
        actor={"type": "user", "id": "alice", "ip": "1.2.3.4"},
        action="user.view",
        resource={"type": "user", "id": 2},
        outcome="success",
    )
    append_audit(
        actor={"type": "user", "id": "admin", "ip": "1.2.3.4"},
        action="user.role_changed",
        resource={"type": "user", "id": 1},
        outcome="success",
        context={"old_role": "user", "new_role": "admin"},
    )

    print(f"\nAudit chain length: {len(audit_chain)}")
    print(f"Chain valid: {verify_audit_chain()}")

    # Simula tampering
    print("\n[Simulazione tampering...]")
    audit_chain[1]["resource"]["id"] = 999     # modifica un'entry
    print(f"Chain valid dopo tampering: {verify_audit_chain()}")
    print("→ Tampering RILEVATO ✓")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        app.run(debug=True, port=5050)


# =====================================================================
# TEST DA TERMINALE
# =====================================================================
#
# Avvio: python M_EXTRA_logging_lab.py
# Demo standalone: python M_EXTRA_logging_lab.py demo
#
# 1) LOGIN OK
#    curl -X POST http://localhost:5050/login \
#      -H "Content-Type: application/json" \
#      -d '{"user":"alice","pwd":"alice123"}'
#    → log JSON con event_type=auth.login.success
#
# 2) LOGIN FAIL ripetuto (brute force)
#    for i in {1..6}; do
#      curl -X POST http://localhost:5050/login \
#        -H "Content-Type: application/json" \
#        -d '{"user":"alice","pwd":"sbagliata"}'
#    done
#    → al 5° fallimento: ALERT brute_force_detected nel security log
#
# 3) DELETE USER (audit)
#    curl -X DELETE http://localhost:5050/users/1 \
#      -H "X-User-Id: admin"
#    → audit log con action=user.delete
#
# 4) PRIVILEGE ESCALATION DETECTION
#    curl -X PUT http://localhost:5050/users/2/role \
#      -H "Content-Type: application/json" \
#      -d '{"role":"admin"}'
#    → security log con event=privilege_escalation severity=high
#
# 5) VERIFY AUDIT CHAIN
#    curl http://localhost:5050/audit/verify
#    → {"valid": true, "entries": N}
#
# 6) INDUCE 500
#    Modifica temporaneamente un endpoint per fare raise.
#    Vedi unhandled_exception nel log.
#
# =====================================================================
# COSA OSSERVARE NELL'OUTPUT
# =====================================================================
#
# Ogni log riga è JSON con:
# - @timestamp ISO 8601 UTC
# - level (INFO/WARNING/ERROR)
# - logger (app/audit/security)
# - msg breve
# - event {action, category, outcome, [severity]}
# - http {request, response}
# - source {ip, user_agent}
# - user {name, id}
# - duration_ms
# - correlation_id (per correlare richieste tra servizi)
#
# Questo formato è ECS-compatibile → ingestibile da Elastic, Splunk, Datadog.
#
# =====================================================================
# ESERCIZI DI APPROFONDIMENTO
# =====================================================================
#
# E1) Aggiungi rate limiting su /login con flask-limiter (5/min).
#     Logga 429 con event=rate_limit_exceeded.
#
# E2) Aggiungi geo-IP detection: se login da paese diverso entro 10 min
#     da quello precedente, alert "geo_anomaly".
#     (Hint: pip install geoip2 + database MaxMind GeoLite2)
#
# E3) Spedisci i log a Elastic Stack:
#     docker run -d -p 9200:9200 -e "discovery.type=single-node" \
#         elasticsearch:8.13.0
#     Modifica il logger per HTTP push a /myapp/_doc.
#
# E4) Fai il diff tra un audit log "buono" e uno "tamperato".
#     Implementa /audit/<id>/check che verifica un singolo entry.
#
# E5) Implementa retention: cancella audit entries > 365 giorni.
#     Salvali su S3 Object Lock prima.
#
# =====================================================================
# DOMANDE DI VERIFICA
# =====================================================================
#
# Q1: Differenza application log vs audit log?
# Q2: Cos'è una hash chain? Perché protegge da tampering?
# Q3: Cosa significa "structured logging"?
# Q4: Cos'è ECS (Elastic Common Schema)?
# Q5: Perché correlation_id è importante in microservizi?
# Q6: Cosa NON va loggato? (almeno 4 cose)
# Q7: Differenza tra SOC tier 1, 2, 3?
"""
