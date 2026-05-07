---
title: "EXTRA — API Security (OWASP API Top 10)"
subtitle: "Corso ITS Cybersecurity — Modulo Avanzato"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# EXTRA — API Security
## 3 ore — OWASP API Top 10 (2023)

## Obiettivi

- Differenze tra API e Webapp
- OWASP API Top 10
- BOLA (la #1)
- BOPLA (mass assignment + excessive data)
- SSRF (caso Capital One)
- Lab FastAPI con difese

## Webapp vs API

| | Webapp | API |
|---|--------|-----|
| Output | HTML | JSON |
| Difese browser | CSP, SameSite | Quasi nessuna |
| Documentazione | Privata | Spesso pubblica (OpenAPI) |
| # Endpoint | 10-50 | Centinaia |
| Authn | Cookie | JWT, API key |

## Tre architetture

```
A) REST/GraphQL stand-alone
B) Backend di SPA/mobile
C) API pubblica per terzi (Stripe, Twilio)
```

Ognuna ha rischi specifici.

## OWASP API Top 10 (2023)

| # | Vulnerabilità |
|---|---------------|
| API1 | **BOLA** |
| API2 | Broken Authentication |
| API3 | **BOPLA** |
| API4 | Unrestricted Resource Consumption |
| API5 | Broken Function Level Authorization |
| API6 | Unrestricted Access to Sensitive Business Flows |
| API7 | **SSRF** |
| API8 | Security Misconfiguration |
| API9 | Improper Inventory Management |
| API10 | Unsafe Consumption of APIs |

## API1 — BOLA

> Broken Object Level Authorization

L'IDOR delle API. **La singola vulnerabilità più diffusa**.

```python
# 🚩
@app.get("/api/users/{uid}/orders")
def list_orders(uid):
    return Order.query.filter_by(user_id=uid).all()
```

## BOLA — Difesa

```python
# ✅ Pattern preferito
@app.get("/api/me/orders")
@require_jwt
def my_orders():
    user_id = request.user["sub"]
    return Order.query.filter_by(user_id=user_id).all()
```

Non usare l'ID dall'URL — usa quello dal token.

## BOLA — Test automatico

```python
def test_bola():
    alice_token = login_as("alice")
    bob_id = users["bob"]["id"]
    r = client.get(f"/api/users/{bob_id}/orders",
                   headers={"Authorization": f"Bearer {alice_token}"})
    assert r.status_code == 403
```

> Per ogni endpoint con ID nell'URL.

## API2 — Broken Authentication

- Login senza rate limit → brute force
- JWT senza scadenza
- Reset password con token prevedibile
- OTP a 4 cifre senza rate limit

## API2 — Difese

- Rate limit aggressivo (5/min su login)
- Account lockout dopo N falliti
- MFA (TOTP, WebAuthn)
- Password policy + HaveIBeenPwned check
- Reset token: random + scadenza 15 min + uso una volta

## API3 — BOPLA Mass Assignment

```python
# 🚩
@app.put("/api/users/{uid}")
def update(uid):
    data = request.json
    user = User.query.get(uid)
    for k, v in data.items():
        setattr(user, k, v)   # accetta QUALSIASI campo
```

Attacco: `{"role": "admin", "is_verified": true}` → privilege escalation.

## BOPLA — Difesa con Pydantic

```python
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    # NO: role, is_admin, balance

@app.put("/api/users/{uid}")
def update(uid, payload: UserUpdate):
    user = User.query.get(uid)
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(user, k, v)
```

## BOPLA — Excessive Data Exposure

```python
# 🚩
return jsonify(User.query.get(uid).__dict__)
# Include password_hash, internal_id, ecc.
```

```python
# ✅
class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr

@app.get("/api/users/{uid}", response_model=UserPublic)
```

FastAPI filtra automaticamente. **Difesa potente.**

## API4 — Resource Consumption

- API senza rate limit
- Query enormi (`?limit=1000000`)
- Upload file no max size
- JSON enormi (Trillion Laughs)

## API4 — Difese

```python
# Rate limit
@limiter.limit("5/minute")

# Pagination cap
limit = min(limit, 100)

# Body size
app.config["MAX_CONTENT_LENGTH"] = 10*1024*1024
```

Per endpoint costosi: code async (Celery), quota giornaliera.

## API5 — Function Level Authz

```python
@app.get("/api/admin/users")
def admin_list():
    # 🚩 controlla solo "esiste token", non "ha role admin"
    return User.query.all()
```

Utente normale chiama → vede tutto.

## API5 — Difesa

```python
@app.get("/api/admin/users")
@require_role("admin")
def admin_list():
    return User.query.all()
```

Pattern: tutti gli endpoint admin sotto `/api/admin/...` con decorator centrale.

## API6 — Sensitive Business Flows

Endpoint legittimi sfruttati in modo non previsto:

- Bot che comprano PS5 al rilascio
- Scraping massivo catalogo
- Account creation farm
- Login stuffing

## API6 — Difese (più comportamentali)

- CAPTCHA su flussi critici
- Device fingerprinting
- Anomaly detection
- Email/SMS verification
- Bot management (Cloudflare, Akamai)

## API7 — SSRF

API accetta URL e fetcha lato server. Attaccante fa fetchare URL **interni**.

```python
# 🚩
@app.post("/fetch-image")
def fetch():
    url = request.json["url"]
    img = requests.get(url).content
```

## SSRF — caso Capital One 2019

100M record clienti rubati.

WAF con SSRF → metadata AWS:
```
http://169.254.169.254/latest/meta-data/iam/security-credentials/
```
→ ruolo IAM con accesso S3 → dump.

Multa $80M + class action.

## SSRF — Difese

- **Whitelist domini** ammessi
- **Blocca IP privati** (10.x, 172.16-31.x, 192.168.x, 169.254.x, 127.x)
- **Blocca protocolli** non-HTTP (file, gopher, ftp)
- **No follow redirect**
- **Network segmentation**: app non raggiunge metadata cloud

## API8 — Misconfiguration

- Debug mode in prod
- Stack trace nelle risposte
- CORS troppo permissivo
- Default credentials
- `Server: nginx/1.18.0` (fingerprint)

## API8 — CORS sottile

```python
# 🚩
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

Con auth via cookie + `*`: pericoloso.

```python
# ✅
CORS(app,
     resources={r"/api/*": {"origins": ["https://app.example.com"]}},
     supports_credentials=True)
```

## API9 — Inventory Management

API "fantasma" o "zombie":

- `/api/v1/users` (vecchia, vulnerabile)
- `/api/internal/admin` (per debug, dimenticata)
- staging.example.com con dati prod

## API9 — Caso Facebook 2021

API GraphQL non documentata permetteva enumerare numeri di telefono.

**533M record leakati**.

> Inventory completo + API gateway centralizzato.

## API10 — Unsafe Consumption

App chiama API terze (Stripe, Twilio) e si fida ciecamente.

**Webhook senza firma**:
```python
# 🚩
@app.post("/webhook/stripe")
def stripe():
    event = request.json
    if event["type"] == "payment_intent.succeeded":
        mark_paid(event["data"]["object"]["id"])
```

Attaccante chiama webhook → ordine pagato senza pagare.

## API10 — Difesa firma webhook

```python
@app.post("/webhook/stripe")
def stripe():
    payload = request.get_data(as_text=True)
    sig = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig, endpoint_secret)
    except SignatureVerificationError:
        abort(400)
```

Stripe firma con HMAC. Solo chi conosce il secret può forgiare evento.

## Lab — FastAPI con difese

Vedi `02_lab/M_EXTRA_api_security_lab.py`.

Include:
- Login con rate limit
- BOLA prevenuto (filtri per token)
- BOPLA prevenuto (Pydantic input/output)
- Function-level authz (admin)
- Test red team

## Test red team

```bash
# BOLA — alice prova ordine di bob → 403
curl /orders/101 -H "Authorization: Bearer $ALICE"

# BOPLA — campo extra ignorato
curl -X PUT /orders/100 -d '{"amount":100,"score":999}'
# score IGNORATO

# Function — alice chiama /admin → 403
curl /admin/orders -H "Authorization: Bearer $ALICE"
```

## Checklist API

Per ogni endpoint:
- [ ] Auth richiesta
- [ ] Authz su oggetto (BOLA)
- [ ] Authz su funzione (admin)
- [ ] Response model whitelist
- [ ] Request model whitelist
- [ ] Rate limit
- [ ] Pagination
- [ ] Pydantic validation
- [ ] Error handler senza stack trace

## Architettura

- [ ] OpenAPI completa
- [ ] API Gateway davanti
- [ ] Versioning + deprecation
- [ ] Network segmentation (no metadata cloud)
- [ ] CORS whitelist precisa
- [ ] HTTPS forzato + HSTS

## Risorse

- OWASP API Top 10 2023
- PortSwigger Academy — API Testing
- 42Crunch Whitepapers
- FastAPI Security docs

## Domande?
