# EXTRA — Logging & Monitoring (OWASP A09)

**Materiale integrativo — Corso ITS Cybersecurity**
**Tipologia**: estensione di M6 (web app security)
**Tempo suggerito**: 2 ore (lettura + lab)
**Prerequisiti**: M3 (HTTP), M6 (web app security)

> **A09 — Security Logging and Monitoring Failures** è nella OWASP Top 10 ma trattata come "trasversale" nel corso base. È in realtà la **differenza tra rilevare un breach in 1 ora o in 200 giorni** (medina del settore: 204 giorni — IBM Cost of a Data Breach Report 2023).

---

## Indice

- [1. Perché il logging è una difesa](#cap1)
- [2. Cosa loggi (e cosa NON loggi)](#cap2)
- [3. Structured logging](#cap3)
- [4. Audit log vs application log](#cap4)
- [5. SIEM ingestion](#cap5)
- [6. Detection patterns](#cap6)
- [7. Alert tuning](#cap7)
- [8. SOC basics](#cap8)
- [9. Lab pratico — Flask con logging strutturato](#cap9)
- [10. Checklist logging](#cap10)

---

<a name="cap1"></a>
## 1. Perché il logging è una difesa

### 1.1 Il numero che fa pensare

> **204 giorni** — tempo medio per identificare un data breach (IBM 2023)
> **73 giorni** — tempo medio per contenerlo
> Totale: **277 giorni** di compromissione tipica.

L'attaccante che non fa rumore e non viene rilevato resta dentro.

### 1.2 Gli unici 3 outcome possibili

Quando viene attaccata, un'azienda ha 3 possibilità:

1. **Non lo sa** (caso comune): scopre dopo mesi quando i dati appaiono in vendita.
2. **Lo sa tardi**: rileva quando il danno è già esteso.
3. **Lo sa subito**: contiene in ore, non giorni.

> La differenza tra 2 e 3 è: **logging + monitoring + alerting funzionanti**.

### 1.3 OWASP A09 — Cosa significa "Failure"

- Eventi importanti **non loggati** (login, accessi sensibili)
- Log **non monitorati**
- Log **modificabili** (niente immutabilità)
- **Nessun alert** automatico
- Alert **ignorati** (alert fatigue)
- Log **insufficienti** per investigazione post-incident

---

<a name="cap2"></a>
## 2. Cosa loggi (e cosa NON loggi)

### 2.1 Cosa DEVI loggare

#### Eventi di autenticazione

- Login OK (user, IP, timestamp, user-agent, mfa_used)
- Login FAIL (user, IP, motivo: wrong-password / account-locked / mfa-fail)
- Logout
- Cambio password
- Reset password (richiesta, completamento)
- Account locked / unlocked
- MFA enrollment, MFA usato

#### Eventi di autorizzazione

- Modifica ruoli/permessi
- Accesso a risorse sensibili (dati personali, finanziari, salute)
- Tentativo di accesso negato (403)
- Privilege escalation tentata o riuscita

#### Eventi business critici

- Transazioni finanziarie (creazione, modifica, conferma)
- Creazione/cancellazione account
- Export di dati
- Modifica dati personali
- Operazioni amministrative

#### Eventi tecnici

- Errori 5xx (con context completo)
- Crash / eccezioni non gestite
- Restart applicazione
- Modifiche configurazione

#### Eventi di sicurezza

- Tentativi di SQLi / XSS rilevati (pattern noti)
- Rate limiting attivato
- Anomaly detection trigger
- Risposta WAF

### 2.2 Cosa NON DEVI loggare (o solo redatto)

🚫 **Mai in chiaro**:

- Password (chiaro, hash, anche temporanee)
- Token completi (logga solo prefisso: `eyJhbGc...`)
- Credit card (PAN intero — solo last 4)
- Codice fiscale, SSN intero (solo redatto)
- Chiavi API
- Cookie di sessione completi
- PII non strettamente necessaria

### 2.3 GDPR e logging

**Caso conflitto**: GDPR vuole minimizzazione, sicurezza vuole loggare tutto.

Risoluzione:
- Logga **identifier** (`user_id=123`), non dati anagrafici (`email=...`).
- **Pseudonimizza** se possibile.
- **Retention** definita (60-90 giorni di solito, più per audit log specifici).
- **Cancellazione** quando l'utente lo richiede (Art. 17 GDPR — diritto all'oblio applicabile anche ai log secondo interpretazione del Garante).
- Log **inclusi** nella DPIA.

### 2.4 Tabella: che dato in che log

| Dato | Log applicativo | Audit log | Note |
|------|-----------------|-----------|------|
| user_id (interno) | ✅ | ✅ | Identifier |
| email | ❌ (eccezione: redatta `m***@example.com`) | ❌ | PII |
| password | ❌ | ❌ | MAI |
| IP | ✅ | ✅ | Diventa PII se persistito >180gg per GDPR |
| user-agent | ✅ | ✅ | Generic |
| Session ID | ❌ (solo prefisso `abc1...`) | ❌ | Token |
| Token | ❌ (solo prefisso) | ❌ | Token |
| Endpoint | ✅ | ✅ | OK |
| Status code | ✅ | ✅ | OK |
| Stack trace | ✅ (interno) | ❌ | Mai al client |

---

<a name="cap3"></a>
## 3. Structured logging

### 3.1 Logging non strutturato (ANTI-PATTERN)

```python
# 🚩 LOG NON STRUTTURATO
logger.info(f"User {user_id} logged in from {ip}")
```

Output:
```
2026-05-06 14:32:15 INFO User 12345 logged in from 1.2.3.4
```

Problema: per cercare "tutti i login dell'utente 12345" → grep + regex fragile. Il SIEM fatica a parsarlo.

### 3.2 Logging strutturato (PATTERN)

```python
# ✅ LOG STRUTTURATO
logger.info("login.success", extra={
    "event_type": "auth.login.success",
    "user_id": user_id,
    "ip": ip,
    "user_agent": user_agent,
    "mfa_used": True,
})
```

Output (JSON):
```json
{
  "ts": "2026-05-06T14:32:15Z",
  "level": "INFO",
  "msg": "login.success",
  "event_type": "auth.login.success",
  "user_id": 12345,
  "ip": "1.2.3.4",
  "user_agent": "Mozilla/5.0...",
  "mfa_used": true
}
```

Vantaggi:
- ✅ SIEM lo ingerisce nativamente
- ✅ Query: `event_type="auth.login.success" AND user_id=12345`
- ✅ Aggregazioni: count by IP per detection brute force
- ✅ Estensibile (aggiungi campi senza rompere parsing)

### 3.3 Implementazione Python

```python
import logging
from pythonjsonlogger import jsonlogger

handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s",
    rename_fields={"asctime": "ts", "levelname": "level"},
))

logger = logging.getLogger("security")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
```

### 3.4 Standard di formato

Due standard principali:

#### **Elastic Common Schema (ECS)**
Standard di Elastic. Campi tipo `event.action`, `user.id`, `source.ip`, `http.request.method`.

#### **OpenTelemetry**
Standard CNCF, più ampio (logs + traces + metrics insieme).

> Usa uno dei due, non un dialetto custom. Faciliterà l'ingestion in SIEM.

### 3.5 Esempio ECS

```python
logger.info("login attempt", extra={
    "event": {
        "action": "login_failed",
        "category": ["authentication"],
        "type": ["start"],
        "outcome": "failure",
    },
    "user": {"name": email_input, "id": None},
    "source": {"ip": request.remote_addr, "user_agent": {"original": ua}},
    "http": {"request": {"method": "POST"}, "response": {"status_code": 401}},
})
```

---

<a name="cap4"></a>
## 4. Audit log vs application log

### 4.1 Differenza

| | Application Log | Audit Log |
|---|-----------------|-----------|
| Scopo | Debug, performance, errori | Tracciabilità azioni utenti |
| Durata | Breve (7-30 gg) | Lunga (2+ anni) |
| Modificabile? | Sì | **No (immutabile)** |
| Volume | Alto | Medio |
| Storage | Hot (Elastic, Splunk) | Cold (S3, archive) |
| Esempio | "DB query took 234ms" | "User 123 deleted record 456" |

### 4.2 Audit log — proprietà richieste

- **Completo**: chi, cosa, quando, dove (IP), risultato.
- **Immutabile**: append-only. Mai modifica/cancella.
- **Sequenziale**: ogni evento ha sequence number monotonic.
- **Verificabile**: hash chain (Merkle-like) per detection tampering.
- **Retention**: 2-7 anni a seconda settore (banche, sanità: 7+).
- **Compliance**: GDPR audit trail Art. 30, NIS 2 Art. 21, SOX (USA).

### 4.3 Esempio di audit log entry

```json
{
  "audit_id": "01HVZAKE2X4...",
  "ts": "2026-05-06T14:32:15.123Z",
  "actor": {"type": "user", "id": 123, "ip": "1.2.3.4"},
  "action": "delete",
  "resource": {"type": "invoice", "id": 456},
  "outcome": "success",
  "context": {"reason": "user request via /invoice/456 DELETE"},
  "prev_hash": "ab12cd34...",
  "self_hash": "ef56gh78..."
}
```

### 4.4 Implementazione audit log immutabile

Pattern:
1. Audit DB **separato** dall'app DB.
2. Solo **INSERT** ammessi (revoca DELETE/UPDATE all'utente DB).
3. **Hash chain**: `self_hash = SHA256(prev_hash + entry_json)`.
4. Backup periodico **append-only** su storage immutabile (S3 Object Lock).

In Python (semplificato):

```python
import hashlib, json, time, ulid

def append_audit(actor, action, resource, outcome, context, prev_hash):
    entry = {
        "audit_id": str(ulid.new()),
        "ts": time.time(),
        "actor": actor,
        "action": action,
        "resource": resource,
        "outcome": outcome,
        "context": context,
        "prev_hash": prev_hash,
    }
    self_hash = hashlib.sha256(
        (prev_hash + json.dumps(entry, sort_keys=True)).encode()
    ).hexdigest()
    entry["self_hash"] = self_hash
    db.audit.insert_one(entry)   # solo INSERT permesso
    return self_hash
```

### 4.5 Detection di tampering

Un job periodico ricalcola gli hash e li confronta. Se uno non torna → log alterato.

---

<a name="cap5"></a>
## 5. SIEM ingestion

### 5.1 Architettura tipica

```
[App Flask] ──stdout JSON──► [Filebeat / Fluent Bit / Vector] ──► [Logstash / Kafka] ──► [Elastic / Splunk]
                                                                         │
                                                                         ▼
                                                                    [Dashboard]
                                                                    [Alert]
                                                                    [SOC]
```

### 5.2 Pattern di ingestion

#### A. **Stdout + log shipper** (12-factor app)

L'app stampa JSON su stdout. Un agente locale (Filebeat, Fluent Bit, Vector) lo legge e invia al SIEM.

```yaml
# filebeat.yml
filebeat.inputs:
  - type: container
    paths: ["/var/log/containers/*.log"]
output.elasticsearch:
  hosts: ["elastic:9200"]
```

Vantaggio: app non sa nulla del SIEM (decoupled).

#### B. **HTTP push diretto**

L'app chiama API del SIEM (Splunk HEC, Elastic _bulk).

```python
import requests
SPLUNK_URL = "https://splunk.example.com/services/collector"
SPLUNK_TOKEN = os.getenv("SPLUNK_HEC_TOKEN")

requests.post(SPLUNK_URL,
    headers={"Authorization": f"Splunk {SPLUNK_TOKEN}"},
    json={"event": entry, "sourcetype": "myapp"},
    timeout=5)
```

Svantaggi: dipendenza, latency, resilience.

#### C. **Message queue**

L'app pubblica su Kafka/RabbitMQ. Consumer SIEM consuma in async. Pattern per high volume.

### 5.3 Best practice

- ✅ Log su stdout in JSON (mai su file diretto, lascia farlo a chi sa).
- ✅ Async send (non bloccare la request per logging).
- ✅ Backpressure: se SIEM down, log buffered locally.
- ✅ Retry con jitter.
- ✅ Drop low-priority log se backlog troppo grande (mai blocking).

---

<a name="cap6"></a>
## 6. Detection patterns

### 6.1 Pattern semplici

#### Brute force login
```
event_type=auth.login.failure | stats count by source.ip span=5m | where count > 10
```
→ alert se più di 10 failed in 5 min dallo stesso IP.

#### Account takeover (login da paese inusuale)
```
1. Calcola "paese tipico" per ogni utente (geo-IP da ultime N session).
2. Se nuovo login viene da paese diverso e a distanza temporale impossibile:
   "alice da Italia alle 14:00, alice da India alle 14:30" → alert.
```

#### Privilege escalation
```
event_type=authz.role_changed | actor.role!=admin | new_role=admin
```
→ alert se non-admin diventa admin. Tipicamente combinato con review.

#### IDOR enumeration
```
event_type=authz.access_denied | http.response.status_code=403
| stats count by user_id, resource.type span=5m
| where count > 30
```
→ utente che riceve 30+ 403 in 5 min sta probabilmente brute-forcing IDOR.

#### Data exfiltration (volume anomalo)
```
event_type=data.export | bytes_exported > NORMAL_BASELINE * 10
```
→ utente che esporta 10x del solito → alert.

### 6.2 Pattern avanzati

- **UEBA** (User and Entity Behavior Analytics): ML che impara comportamento normale, alert su deviazioni.
- **Threat intelligence integration**: blocca/alert su IP in liste TI (TOR exit, malicious infra).
- **Correlation**: 5 failed login + 1 success = alert (probabile credential stuffing riuscito).

### 6.3 MITRE ATT&CK come guida

Il framework **ATT&CK** elenca tattiche e tecniche di attaccanti reali. Ogni tecnica suggerisce log da raccogliere.

Esempio: tecnica T1110 (Brute Force) → suggerisce di loggare login failure pattern, password spray.

---

<a name="cap7"></a>
## 7. Alert tuning

### 7.1 Il problema dell'alert fatigue

Ricerca Trend Micro 2023: SOC riceve **mediamente 11.000 alert al giorno**. Solo **30%** investigato. Tra questi, **molti falsi positivi**.

Risultato: alert reali si perdono.

### 7.2 Principi di tuning

- **Severity tiers**: Critical, High, Medium, Low.
- **Critical = page** (24/7, anche di notte).
- **High = ticket** (in giornata).
- **Medium/Low = batch review** (settimanale).
- **Tune mensilmente**: alert con >50% false positive vanno rivisti o disabilitati.

### 7.3 Esempio gerarchia per webapp

| Pattern | Severity | Action |
|---------|----------|--------|
| 100+ failed login da 1 IP in 1 min | High | Block IP, alert SOC |
| 1 failed login | None | Solo log |
| Account takeover (geo + time) | Critical | Lock account, alert SOC + utente |
| Stack trace su 500 in prod | Medium | Ticket dev team |
| 1 SQL injection pattern in WAF | Low | Log |
| 50+ SQLi pattern in 5 min | High | Alert + WAF rule update |
| Modifica role to admin | Critical | Alert SOC + verify |
| Export di >1GB di dati | High | Verify autorizzato |
| 1000 login OK in 1 ora | Medium | Investigate (può essere legit) |

### 7.4 Playbook di risposta

Per ogni alert critical, deve esistere un **playbook**:

1. **Cosa significa** l'alert?
2. **Verifica** rapida (è falso positivo?)
3. **Contenimento** (blocca IP, lock account, ecc.)
4. **Indagine** (cosa è successo? Quanto è esteso?)
5. **Eradicazione** (rimuovi malware, ruota credenziali)
6. **Recovery** (ripristina servizio)
7. **Lessons learned** (post-mortem)

---

<a name="cap8"></a>
## 8. SOC basics

### 8.1 Cos'è un SOC

**Security Operations Center**. Team che monitora il SIEM, risponde agli alert, investiga, contiene.

### 8.2 Tier 1, 2, 3

- **Tier 1**: front line. Triagia gli alert, risolve i banali, escalate i complessi.
- **Tier 2**: investiga, fa forensics, contiene.
- **Tier 3**: senior. Caccia minacce avanzate (threat hunting), analisi malware, advisor.

### 8.3 SOC interno vs MSSP

- **Interno**: costoso (24/7 = ~10 persone), serve scala.
- **MSSP** (Managed Security Service Provider): outsourced. Più conveniente per medie aziende.
- **MDR** (Managed Detection & Response): MSSP focalizzato su detection + response.
- **XDR** (Extended Detection & Response): piattaforme che fanno detection cross-domain (endpoint + email + cloud + network).

### 8.4 Dal punto di vista app developer

Se la tua azienda ha un SOC, il tuo **dovere** come dev è:

1. **Loggare bene** (vedi cap 2).
2. **Esporre webhook/integrazioni** (es. lock account on demand).
3. **Documentare** dove sono i log, quale formato.
4. **Collaborare** durante incident (puoi spiegare cosa fa il codice).

> Il SOC non sa programmare. Tu lo sai. Insieme funziona.

---

<a name="cap9"></a>
## 9. Lab pratico — Flask con logging strutturato

### 9.1 Setup

```bash
pip install flask python-json-logger
```

### 9.2 Codice

```python
# app.py
import logging
import time
from functools import wraps
from flask import Flask, request, jsonify, g
from pythonjsonlogger import jsonlogger

# === SETUP LOGGING ===
def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"asctime": "ts", "levelname": "level", "name": "logger"},
    ))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]
    return logging.getLogger("app")

log = setup_logging()
audit_log = logging.getLogger("audit")

app = Flask(__name__)


# === MIDDLEWARE: log request ===
@app.before_request
def before():
    g.start = time.time()

@app.after_request
def after(response):
    elapsed_ms = (time.time() - g.start) * 1000
    log.info("http_request", extra={
        "event": {"action": "http.request", "outcome": "success" if response.status_code < 400 else "failure"},
        "http": {
            "request": {"method": request.method, "url": request.url},
            "response": {"status_code": response.status_code},
        },
        "source": {"ip": request.remote_addr, "user_agent": request.user_agent.string},
        "duration_ms": round(elapsed_ms, 2),
    })
    return response


# === DECORATOR: audit per azioni critiche ===
def audit_action(action_type):
    def deco(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_id = request.headers.get("X-User-Id", "anonymous")
            try:
                result = f(*args, **kwargs)
                outcome = "success"
                return result
            except Exception as e:
                outcome = "failure"
                raise
            finally:
                audit_log.info(action_type, extra={
                    "event": {"action": action_type, "category": ["audit"], "outcome": outcome},
                    "user": {"id": user_id},
                    "source": {"ip": request.remote_addr},
                    "http": {"request": {"method": request.method, "url": request.url}},
                })
        return wrapper
    return deco


# === ENDPOINTS ===
USERS = {1: {"name": "Alice"}, 2: {"name": "Bob"}}

@app.post("/login")
def login():
    user = request.json.get("user")
    pwd = request.json.get("pwd")

    # Simulazione
    if user == "alice" and pwd == "alice123":
        log.info("auth.login.success", extra={
            "event": {"action": "auth.login", "outcome": "success"},
            "user": {"name": user},
            "source": {"ip": request.remote_addr},
        })
        return jsonify({"token": "fake-token"})
    else:
        log.warning("auth.login.failure", extra={
            "event": {"action": "auth.login", "outcome": "failure",
                     "reason": "invalid_credentials"},
            "user": {"name": user},
            "source": {"ip": request.remote_addr},
        })
        return jsonify({"error": "invalid"}), 401


@app.delete("/users/<int:uid>")
@audit_action("user.delete")
def delete_user(uid):
    if uid not in USERS:
        return jsonify({"error": "not found"}), 404
    del USERS[uid]
    return jsonify({"deleted": uid})


@app.errorhandler(Exception)
def handle_error(e):
    log.exception("unhandled_exception", extra={
        "event": {"action": "error.unhandled", "outcome": "failure"},
    })
    return jsonify({"error": "internal"}), 500


if __name__ == "__main__":
    app.run(debug=False, port=5000)
```

### 9.3 Test

```bash
# Run
python app.py

# In altro terminale: prova login OK
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"user":"alice","pwd":"alice123"}'

# Login fail
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"user":"alice","pwd":"sbagliata"}'

# Delete (audit)
curl -X DELETE http://localhost:5000/users/1 -H "X-User-Id: 999"
```

Output stdout (esempio):

```json
{"ts": "2026-05-06...", "level": "INFO", "logger": "app", "message": "auth.login.success", "event": {...}, "user": {...}}
{"ts": "2026-05-06...", "level": "INFO", "logger": "audit", "message": "user.delete", "event": {...}, "user": {"id": "999"}}
```

### 9.4 Esercizio — detection brute force

Usa `tail -f` su un file di log o ingerisci in Elastic. Conta failed login per IP in finestre di 1 minuto. Alert se >5.

```python
# Esempio detection inline (in produzione: SIEM)
from collections import defaultdict
from datetime import datetime, timedelta

failed_logins = defaultdict(list)

def record_failed_login(ip):
    now = datetime.now()
    failed_logins[ip] = [t for t in failed_logins[ip] if now - t < timedelta(minutes=1)]
    failed_logins[ip].append(now)
    if len(failed_logins[ip]) > 5:
        log.error("brute_force_detected", extra={
            "event": {"action": "security.brute_force", "outcome": "alert"},
            "source": {"ip": ip},
            "count": len(failed_logins[ip]),
        })
        # In prod: blocca IP, notifica SOC, ecc.
```

---

<a name="cap10"></a>
## 10. Checklist logging

### 10.1 Per chi sviluppa app

- [ ] Logging strutturato JSON (ECS o OTel)
- [ ] Stdout (no file diretti)
- [ ] Logga tutti gli eventi auth (success + failure)
- [ ] Logga 4xx con context (chi, dove, perché)
- [ ] Logga 5xx con stack trace **interno**, mai al client
- [ ] Audit log separato per azioni critiche
- [ ] Timestamp UTC ISO 8601
- [ ] Correlation ID (request-id) tra log
- [ ] No PII in chiaro
- [ ] No password / token / cookie completi
- [ ] Hash chain per audit log (immutabile)

### 10.2 Per architettura

- [ ] Log shipper (Filebeat/Fluent Bit)
- [ ] SIEM o aggregatore centrale
- [ ] Retention definita (con consenso GDPR)
- [ ] Backup audit log su storage immutabile
- [ ] Network: solo SIEM legge i log (niente accessi diretti)

### 10.3 Per detection

- [ ] Detection rules per scenari critici (brute force, IDOR, exfiltration)
- [ ] Severity tiers definiti
- [ ] Alert tuning mensile
- [ ] Playbook per ogni alert critical
- [ ] Dashboard di SOC operativo

### 10.4 Per compliance

- [ ] Audit log conforme GDPR (Art. 32)
- [ ] Audit log conforme NIS 2 (Art. 21)
- [ ] Retention compatibile con normativa settore
- [ ] Procedure cancellazione log (GDPR Art. 17)
- [ ] DPO informato di cosa logghi

---

## Per approfondire

- **OWASP Logging Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- **Elastic Common Schema**: https://www.elastic.co/guide/en/ecs/current/index.html
- **OpenTelemetry Logs**: https://opentelemetry.io/docs/specs/otel/logs/
- **MITRE ATT&CK**: https://attack.mitre.org
- **NIST SP 800-92** (Guide to Log Management): https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf
- **IBM Cost of a Data Breach Report**: https://www.ibm.com/security/data-breach (annuale, gratuito)

---

> **Suggerimento di integrazione**:
> - 1.5h aggiuntive a M6.6 (ora supply chain) → diventa "M6.6 Supply Chain & Logging"
> - Capitolo principale di un eventuale "Modulo SOC/Blue Team"
