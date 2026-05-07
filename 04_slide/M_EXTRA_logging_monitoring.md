---
title: "EXTRA — Logging & Monitoring (OWASP A09)"
subtitle: "Corso ITS Cybersecurity — Modulo Avanzato"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# EXTRA — Logging & Monitoring
## 2 ore — OWASP A09, audit log, SIEM, SOC

## Obiettivi

- Perché il logging è una difesa
- Cosa loggi (e cosa no)
- Structured logging (ECS, OpenTelemetry)
- Audit log immutabile
- SIEM ingestion
- Detection patterns
- SOC basics

## Il numero che fa pensare

> **204 giorni** — tempo medio per identificare un breach
> **73 giorni** — tempo medio per contenerlo
> **Totale: 277 giorni** di compromissione tipica
>
> *(IBM Cost of a Data Breach Report 2023)*

## I 3 outcome possibili

Quando un'azienda viene attaccata:

1. **Non lo sa** (caso comune): scopre quando i dati sono in vendita
2. **Lo sa tardi**: rileva quando il danno è esteso
3. **Lo sa subito**: contiene in ore

> Differenza 2→3: **logging + monitoring + alerting**.

## OWASP A09 — Cosa significa Failure

- Eventi importanti **non loggati**
- Log **non monitorati**
- Log **modificabili** (no immutabilità)
- **Nessun alert** automatico
- Alert **ignorati** (fatigue)
- Log **insufficienti** per investigazione

## Cosa DEVI loggare — Auth

- Login OK (user, IP, MFA, UA)
- Login FAIL (motivo: wrong-pw, locked, mfa-fail)
- Logout
- Cambio password
- Reset password (richiesta + completamento)
- Account locked / unlocked
- MFA enrollment / uso

## Cosa DEVI loggare — Authz

- Modifica ruoli/permessi
- Accesso a risorse sensibili
- Tentativi accesso negato (403)
- Privilege escalation tentata/riuscita

## Cosa DEVI loggare — Business

- Transazioni (creazione, modifica, conferma)
- Creazione/cancellazione account
- Export dati
- Modifica dati personali
- Operazioni amministrative

## Cosa DEVI loggare — Tecnico

- Errori 5xx con context completo
- Crash / eccezioni non gestite
- Restart applicazione
- Modifiche configurazione
- Tentativi SQLi/XSS rilevati
- Rate limit attivato
- Anomaly detection

## Cosa NON DEVI loggare

🚫 Mai in chiaro:
- Password (anche temporanee)
- Token completi (solo prefisso)
- Carta credito intera (solo last 4)
- CF / SSN intero
- Chiavi API
- Cookie sessione completi
- PII non strettamente necessaria

## GDPR vs logging

Conflitto: GDPR vuole minimizzazione, sicurezza vuole loggare.

Risoluzione:
- **Identifier** (`user_id=123`), non email
- **Pseudonimizza** dove possibile
- **Retention** definita (60-90gg)
- **Cancellazione** su richiesta (Art. 17)
- Log **inclusi** nella DPIA

## Cosa va in che log

| Dato | App log | Audit log |
|------|---------|-----------|
| user_id interno | ✅ | ✅ |
| email | ❌ (o redatta) | ❌ |
| password | ❌ MAI | ❌ MAI |
| IP | ✅ | ✅ |
| Session ID | solo prefisso | solo prefisso |
| Stack trace | ✅ interno | ❌ |

## Logging non strutturato — antipattern

```python
# 🚩
logger.info(f"User {uid} logged in from {ip}")
```

Output:
```
2026-05-06 14:32 INFO User 123 logged in from 1.2.3.4
```

Problema: grep + regex fragile. SIEM fatica.

## Structured logging — pattern

```python
# ✅
logger.info("login.success", extra={
    "event_type": "auth.login.success",
    "user_id": uid,
    "ip": ip,
    "user_agent": ua,
    "mfa_used": True,
})
```

Output JSON.

## Implementazione Python

```python
from pythonjsonlogger import jsonlogger
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(message)s",
    rename_fields={"asctime": "ts", "levelname": "level"},
))
```

## Standard di formato

| Standard | Note |
|----------|------|
| **Elastic Common Schema (ECS)** | Standard Elastic, campi `event.action`, `user.id` |
| **OpenTelemetry** | CNCF, logs+traces+metrics |

> Usa uno dei due. Non dialetto custom.

## Esempio ECS

```python
logger.info("login attempt", extra={
    "event": {
        "action": "login_failed",
        "category": ["authentication"],
        "outcome": "failure",
    },
    "user": {"name": email_input},
    "source": {"ip": request.remote_addr},
    "http": {"response": {"status_code": 401}},
})
```

## Application log vs Audit log

| | App log | Audit log |
|---|---------|-----------|
| Scopo | Debug, errori | Tracciabilità azioni |
| Durata | Breve (7-30gg) | Lunga (2+ anni) |
| Modificabile? | Sì | **No** |
| Volume | Alto | Medio |
| Storage | Hot | Cold |

## Audit log — proprietà

- **Completo**: chi/cosa/quando/dove/risultato
- **Immutabile**: append-only
- **Sequenziale**: monotonic seq
- **Verificabile**: hash chain
- **Retention**: 2-7 anni
- **Compliance**: GDPR Art. 30, NIS 2 Art. 21, SOX

## Audit log — esempio

```json
{
  "audit_id": "01HVZAKE2X4...",
  "ts": "2026-05-06T14:32:15Z",
  "actor": {"type": "user", "id": 123, "ip": "1.2.3.4"},
  "action": "delete",
  "resource": {"type": "invoice", "id": 456},
  "outcome": "success",
  "prev_hash": "ab12cd...",
  "self_hash": "ef56gh..."
}
```

## Audit log immutabile — pattern

1. Audit DB **separato** dall'app DB
2. Solo INSERT (no DELETE/UPDATE per app user)
3. **Hash chain**: `self = SHA256(prev + entry)`
4. Backup append-only su S3 Object Lock

## Hash chain — codice

```python
def append_audit(actor, action, resource, prev_hash):
    entry = {
        "audit_id": str(ulid.new()),
        "ts": time.time(),
        "actor": actor, "action": action,
        "resource": resource,
        "prev_hash": prev_hash,
    }
    self_hash = hashlib.sha256(
        (prev_hash + json.dumps(entry, sort_keys=True)).encode()
    ).hexdigest()
    entry["self_hash"] = self_hash
    db.audit.insert_one(entry)
    return self_hash
```

Job periodico ricalcola → tampering rilevato.

## SIEM — architettura

```
[App] ─stdout JSON─► [Filebeat/Vector] ─► [Logstash/Kafka] ─► [Elastic/Splunk]
                                                                    │
                                                                    ▼
                                                              [Dashboard]
                                                              [Alert] [SOC]
```

## SIEM — pattern di ingestion

| Pattern | Note |
|---------|------|
| Stdout + log shipper | 12-factor, decoupled ✅ |
| HTTP push diretto | App sa del SIEM |
| Message queue (Kafka) | High volume |

## Best practice ingestion

- Log su stdout (no file diretti)
- Async send (non bloccare request)
- Backpressure: SIEM down → buffer locale
- Retry con jitter
- Drop low-priority se backlog

## Detection — Brute force

```
event_type=auth.login.failure
| stats count by source.ip span=5m
| where count > 10
```

> 10+ failed in 5 min stesso IP → alert

## Detection — Account takeover

```
1. Calcola "paese tipico" per ogni utente
2. Login da paese diverso a distanza temporale impossibile:
   "alice da Italia 14:00, alice da India 14:30"
   → alert
```

## Detection — Privilege escalation

```
event_type=authz.role_changed
| actor.role!=admin | new_role=admin
```

> Non-admin diventa admin → alert + review

## Detection — IDOR enumeration

```
event_type=authz.access_denied
| http.response.status_code=403
| stats count by user_id span=5m
| where count > 30
```

> 30+ 403 in 5 min stesso user → brute-forcing IDOR

## Detection — Exfiltration

```
event_type=data.export
| bytes_exported > NORMAL_BASELINE * 10
```

> Volume 10x del solito → alert

## Pattern avanzati

- **UEBA**: ML su comportamento
- **Threat intelligence**: blocca IP in liste TI (TOR, malicious)
- **Correlation**: 5 fail + 1 success = credential stuffing riuscito

## Alert fatigue

> SOC riceve **mediamente 11.000 alert/giorno**.
> Solo **30% investigati**. Tra questi, molti falsi positivi.
>
> Risultato: alert reali si perdono.

## Tuning principles

- **Severity tiers**: Critical, High, Medium, Low
- **Critical** = page (24/7)
- **High** = ticket (in giornata)
- **Medium/Low** = batch review settimanale
- **Tune mensile**: alert con >50% FP da rivedere

## Esempio gerarchia

| Pattern | Severity |
|---------|----------|
| 100+ fail login da IP in 1 min | High |
| Account takeover | Critical |
| Stack trace su 500 prod | Medium |
| 50+ SQLi pattern in 5 min | High |
| Modifica role to admin | Critical |
| Export >1GB | High |

## Playbook per alert critical

1. **Cosa significa** l'alert?
2. **Verifica** rapida (FP?)
3. **Contenimento**
4. **Indagine**
5. **Eradicazione**
6. **Recovery**
7. **Lessons learned**

## SOC tier

| Tier | Cosa fa |
|------|---------|
| **1** | Triagia, risolve banali, escalate |
| **2** | Investiga, forensics, contiene |
| **3** | Threat hunting, malware analysis |

## SOC interno vs MSSP

- **Interno**: costoso (24/7 = ~10 persone)
- **MSSP**: outsourced
- **MDR**: detection+response gestita
- **XDR**: cross-domain (endpoint+email+cloud+network)

## Per il dev: cosa serve fare

Se la tua azienda ha SOC, **dovere developer**:

1. Loggare bene
2. Esporre webhook/integrazioni (lock account on demand)
3. Documentare formato/posizione log
4. Collaborare durante incident

> SOC non sa programmare. Tu sì.

## Lab — Flask logging strutturato

`02_lab/M_EXTRA_logging_lab.py`

Include:
- JSON logging ECS-style
- Middleware before/after request
- Decorator @audit_action
- Brute force detection inline
- Alert su pattern

## Checklist sviluppo

- [ ] Logging strutturato JSON
- [ ] Stdout, no file diretti
- [ ] Tutti gli eventi auth
- [ ] 4xx con context
- [ ] 5xx con stack trace **interno**
- [ ] Audit log separato
- [ ] Timestamp UTC ISO 8601
- [ ] Correlation ID
- [ ] No PII chiaro
- [ ] No password/token interi
- [ ] Hash chain audit

## Checklist architettura

- [ ] Log shipper (Filebeat)
- [ ] SIEM aggregato
- [ ] Retention definita (GDPR)
- [ ] Backup audit immutabile
- [ ] Network: solo SIEM legge log

## Checklist detection

- [ ] Detection rules per scenari critici
- [ ] Severity tiers
- [ ] Tuning mensile
- [ ] Playbook per alert critical
- [ ] Dashboard SOC operativo

## Risorse

- OWASP Logging Cheat Sheet
- Elastic Common Schema
- OpenTelemetry Logs
- MITRE ATT&CK
- NIST SP 800-92
- IBM Cost of a Data Breach Report

## Domande?
