# EXTRA — API Security (OWASP API Security Top 10)

**Materiale integrativo — Corso ITS Cybersecurity**
**Tipologia**: estensione di M3 (HTTP) e M6 (web app security)
**Tempo suggerito**: 3 ore (lettura + lab)
**Prerequisiti**: M3 (HTTP, REST), M6 (OWASP Top 10 web)

> Le API REST/GraphQL hanno **vulnerabilità diverse** dalle webapp tradizionali. OWASP ha una lista dedicata: **OWASP API Security Top 10**, aggiornata 2023.

---

## Indice

- [1. Perché API ≠ Web App](#cap1)
- [2. OWASP API Security Top 10 (2023)](#cap2)
- [3. API1 — BOLA (Broken Object Level Authorization)](#cap3)
- [4. API2 — Broken Authentication](#cap4)
- [5. API3 — BOPLA (Broken Object Property Level Authorization)](#cap5)
- [6. API4 — Unrestricted Resource Consumption](#cap6)
- [7. API5 — Broken Function Level Authorization](#cap7)
- [8. API6 — Unrestricted Access to Sensitive Business Flows](#cap8)
- [9. API7 — Server-Side Request Forgery (SSRF)](#cap9)
- [10. API8 — Security Misconfiguration](#cap10)
- [11. API9 — Improper Inventory Management](#cap11)
- [12. API10 — Unsafe Consumption of APIs](#cap12)
- [13. Lab pratico — FastAPI con difese](#cap13)
- [14. Checklist API Security](#cap14)

---

<a name="cap1"></a>
## 1. Perché API ≠ Web App

Le API hanno superficie di attacco diversa:

| Aspetto | Webapp tradizionale | API |
|---------|---------------------|-----|
| **Output** | HTML | JSON/XML |
| **Difese browser** | CSP, SameSite | Quasi nessuna |
| **Documentazione** | Privata | Spesso pubblica (OpenAPI/Swagger) |
| **Volume di endpoint** | 10-50 | Centinaia/migliaia |
| **Authn** | Cookie + sessione | JWT, OAuth, API key |
| **Authz** | Spesso poco granulare | Su ogni oggetto |

**Conseguenze**:
- XSS è meno impattante (no rendering HTML).
- BOLA/IDOR è la vulnerabilità #1 delle API (e di gran lunga).
- Il client (mobile, SPA) **non è fidato**: ogni check va lato server.
- Documentation expose pattern → enumeration banale.

---

<a name="cap2"></a>
## 2. OWASP API Security Top 10 (2023)

| Codice | Vulnerabilità |
|--------|---------------|
| **API1** | Broken Object Level Authorization (BOLA) |
| **API2** | Broken Authentication |
| **API3** | Broken Object Property Level Authorization (BOPLA) |
| **API4** | Unrestricted Resource Consumption |
| **API5** | Broken Function Level Authorization |
| **API6** | Unrestricted Access to Sensitive Business Flows |
| **API7** | Server-Side Request Forgery (SSRF) |
| **API8** | Security Misconfiguration |
| **API9** | Improper Inventory Management |
| **API10** | Unsafe Consumption of APIs |

> **API1 (BOLA) è la vulnerabilità singolarmente più diffusa** in tutte le API testate. Praticamente l'IDOR del corso M6.3 — ma scrivere "BOLA" è più professionale nel contesto API.

---

<a name="cap3"></a>
## 3. API1 — BOLA (Broken Object Level Authorization)

### 3.1 Cos'è

L'IDOR delle API. L'utente loggato accede a oggetti **non suoi** semplicemente cambiando un ID.

### 3.2 Esempio

```python
# 🚩 VULNERABILE
@app.get("/api/users/{user_id}/orders")
def list_orders(user_id: int):
    return Order.query.filter_by(user_id=user_id).all()
```

Attacco: `GET /api/users/43/orders` → vedo gli ordini di un altro.

### 3.3 Difesa — ownership check

```python
# ✅ SICURO
@app.get("/api/users/{user_id}/orders")
@require_jwt
def list_orders(user_id: int):
    if request.user["sub"] != str(user_id) and "admin" not in request.user["roles"]:
        abort(403)
    return Order.query.filter_by(user_id=user_id).all()
```

**Pattern preferito** — non usare l'ID dall'URL ma dal token:

```python
# ✅ ANCORA MEGLIO
@app.get("/api/me/orders")
@require_jwt
def my_orders():
    user_id = request.user["sub"]
    return Order.query.filter_by(user_id=user_id).all()
```

### 3.4 Test automatici

```python
def test_bola_orders(client):
    # Login come alice
    alice_token = login_as("alice")
    bob_id = users["bob"]["id"]

    # Alice prova a leggere ordini di bob
    r = client.get(f"/api/users/{bob_id}/orders",
                   headers={"Authorization": f"Bearer {alice_token}"})

    assert r.status_code == 403, "BOLA: alice ha letto ordini di bob"
```

> **Da fare per ogni endpoint con ID nell'URL**.

---

<a name="cap4"></a>
## 4. API2 — Broken Authentication

### 4.1 Esempi

- Endpoint `/api/login` senza rate limit → brute force
- Token JWT senza scadenza
- Reset password con token prevedibile
- OTP a 4 cifre senza rate limit
- Refresh token senza rotation (vedi EXTRA JWT)

### 4.2 Difese

- **Rate limit aggressivo** sul login (es. 5 tentativi/min per IP)
- **Account lockout** dopo N falliti
- **MFA** (TOTP, WebAuthn)
- **Password policy**: ≥12 char, no top-100 leaked (HaveIBeenPwned API)
- **Token con scadenza** + rotation
- Reset password con **token random crittograficamente sicuro** + scadenza breve (15 min) + uso una volta

---

<a name="cap5"></a>
## 5. API3 — BOPLA (Broken Object Property Level Authorization)

### 5.1 Mass Assignment

```python
# 🚩 VULNERABILE
@app.put("/api/users/{user_id}")
def update_user(user_id: int):
    data = request.json
    user = User.query.get(user_id)
    for key, val in data.items():
        setattr(user, key, val)   # ⚠️ accetta QUALSIASI campo
    db.commit()
```

Attacco:
```bash
curl -X PUT /api/users/me -d '{"role": "admin", "is_verified": true}'
```

L'utente modifica campi che non dovrebbe poter modificare (privilege escalation).

### 5.2 Difesa — whitelist campi

```python
# ✅ SICURO con Pydantic
from pydantic import BaseModel

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    # NON includere "role", "is_admin", "balance"

@app.put("/api/users/{user_id}")
def update_user(user_id: int, payload: UserUpdate):
    user = User.query.get(user_id)
    for key, val in payload.dict(exclude_unset=True).items():
        setattr(user, key, val)
    db.commit()
```

### 5.3 Excessive Data Exposure

```python
# 🚩 VULNERABILE
@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    return jsonify(User.query.get(user_id).__dict__)
    # Restituisce password_hash, internal_id, ecc.
```

### 5.4 Difesa — response model

```python
# ✅ SICURO
class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    # NON: password_hash, role, ip_logs

@app.get("/api/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int):
    return User.query.get(user_id)
```

In FastAPI, `response_model` filtra automaticamente i campi non dichiarati. **Difesa potente e semplice**.

---

<a name="cap6"></a>
## 6. API4 — Unrestricted Resource Consumption

### 6.1 Esempi

- API senza rate limit → DoS via bombardamento
- Endpoint che permette query enormi (`?limit=1000000`)
- Upload file senza max size → riempi disco
- Endpoint che processa input grandi (parse JSON con Trillion Laughs, ecc.)

### 6.2 Difese

#### Rate limiting

```python
# Flask-Limiter
from flask_limiter import Limiter

limiter = Limiter(get_remote_address, app=app)

@app.route("/api/login")
@limiter.limit("5 per minute")
def login(): ...
```

#### Pagination obbligatoria

```python
# ✅ Pagination con cap
@app.get("/api/orders")
def list_orders(limit: int = 20, offset: int = 0):
    limit = min(limit, 100)   # cap a 100
    return Order.query.limit(limit).offset(offset).all()
```

#### Max body size

In Flask:
```python
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024   # 10MB
```

#### Timeout

```python
# Flask con werkzeug
app.config["TIMEOUT"] = 30
```

#### Cost-based limiting

Per endpoint costosi (export CSV, report):
- Code asincrone (Celery, RQ)
- Quota giornaliera utente
- Pricing tier-based

---

<a name="cap7"></a>
## 7. API5 — Broken Function Level Authorization

### 7.1 Esempio

```python
@app.get("/api/admin/users")
def admin_list_users():
    # 🚩 controllo solo "esiste un token", non "ha ruolo admin"
    return User.query.all()
```

L'utente normale può chiamare endpoint admin se conosce l'URL.

### 7.2 Difesa

```python
@app.get("/api/admin/users")
@require_role("admin")
def admin_list_users():
    return User.query.all()
```

### 7.3 Pattern strutturale

- **Naming convention**: tutti gli endpoint admin sotto `/api/admin/...`
- **Decorator centralizzato**: `@require_role("admin")` su tutti
- **Test automatico**: per ogni endpoint admin, test che user normale riceve 403.

---

<a name="cap8"></a>
## 8. API6 — Unrestricted Access to Sensitive Business Flows

### 8.1 Cos'è

Endpoint legittimi ma sfruttabili in **modi non previsti** dalla business logic.

### 8.2 Esempi

- **Bot che comprano prodotti limitati** (PS5, sneakers) appena disponibili.
- **Scraping massivo** del catalogo competitor.
- **Account creation farm** per voti, recensioni, ecc.
- **Login stuffing** con liste di credenziali rubate.

### 8.3 Difese

- **CAPTCHA** (reCAPTCHA, hCaptcha) sui flussi critici.
- **Device fingerprinting** (FingerprintJS).
- **Anomaly detection** comportamentale (es. 100 ordini in 1 secondo dallo stesso IP).
- **Email/SMS verification** per registrazione.
- **Bot management** (Cloudflare, Akamai).

> Difesa più **comportamentale** che tecnica. Il bot fa cose che un umano non farebbe.

---

<a name="cap9"></a>
## 9. API7 — Server-Side Request Forgery (SSRF)

### 9.1 Cos'è

L'API accetta un URL dall'utente e ne fa la fetch lato server. L'attaccante fa fetchare URL **interni** (cloud metadata, intranet).

### 9.2 Esempio

```python
# 🚩 VULNERABILE
@app.post("/api/fetch-image")
def fetch_image():
    url = request.json["url"]
    img = requests.get(url).content
    save(img)
```

Attacco classico (AWS):
```bash
curl /api/fetch-image -d '{"url":"http://169.254.169.254/latest/meta-data/iam/security-credentials/"}'
```

→ leak credenziali AWS della macchina.

### 9.3 Caso reale — Capital One 2019

- 100M record clienti rubati
- WAF di Capital One con SSRF → metadata AWS → ruolo IAM con accesso S3
- Multa $80M + class action

### 9.4 Difese

- **Whitelist domini** ammessi.
- **Bloccare IP privati** (10.x, 172.16-31.x, 192.168.x, 169.254.x, 127.x, ::1).
- **Bloccare protocolli non-HTTP** (`file://`, `gopher://`, `ftp://`).
- **Disabilitare follow redirect** (o limitare a 1).
- **Network segmentation**: il server applicativo non deve poter raggiungere metadata cloud.

```python
import ipaddress
from urllib.parse import urlparse
import socket

ALLOWED_DOMAINS = {"images.example.com", "cdn.example.com"}

def safe_fetch(url: str) -> bytes:
    p = urlparse(url)
    if p.scheme not in {"http", "https"}:
        raise ValueError("schema non ammesso")
    if p.hostname not in ALLOWED_DOMAINS:
        raise ValueError("dominio non in whitelist")

    # Risolvi e blocca IP privati
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(p.hostname))
    except (socket.gaierror, ValueError):
        raise ValueError("hostname non risolvibile")
    if ip.is_private or ip.is_loopback or ip.is_link_local:
        raise ValueError("IP privato vietato")

    return requests.get(url, timeout=5, allow_redirects=False).content
```

---

<a name="cap10"></a>
## 10. API8 — Security Misconfiguration

### 10.1 Esempi tipici

- **Debug mode in produzione** (Flask `debug=True`, Django `DEBUG=True`)
- **Stack trace nelle risposte 500**
- **CORS troppo permissivo** (`Access-Control-Allow-Origin: *` per API auth)
- **Headers di sicurezza mancanti**
- **Default credentials** (admin/admin)
- **OPTIONS verb** che espone tutta la struttura
- **Verbose `Server` header** (nginx 1.18.0)

### 10.2 CORS — il caso più sottile

```python
# 🚩 VULNERABILE
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

Con autenticazione via cookie, `Access-Control-Allow-Origin: *` **NON è permesso** se anche `Allow-Credentials: true`. Ma se l'app risponde così → browser non blocca i moderni → attacker da `evil.com` può fare richieste autenticate.

```python
# ✅ SICURO
CORS(app,
     resources={r"/api/*": {"origins": ["https://app.example.com"]}},
     supports_credentials=True)
```

### 10.3 Difesa generale — hardening checklist

- [ ] `DEBUG = False` in prod (verifica in CI)
- [ ] Error handler globale 500 che NON mostra stack trace
- [ ] CORS con origin whitelist precisa
- [ ] Headers di sicurezza (vedi M3)
- [ ] Niente default credentials nel deploy
- [ ] `Server` rimosso o offuscato

---

<a name="cap11"></a>
## 11. API9 — Improper Inventory Management

### 11.1 Cos'è

API "**fantasma**" o "**zombie**" che esistono ma non sono documentate, monitorate, patchate.

### 11.2 Esempi

- `/api/v1/users` (vecchia versione, ancora attiva, vulnerabile)
- `/api/internal/admin` (per debug, dimenticata)
- `staging.example.com` accessibile da Internet con dati di prod
- Endpoint generato da framework (es. `/_debug/`)

### 11.3 Caso reale

- **Facebook 2021**: API GraphQL non documentata che permetteva enumerazione di numeri di telefono. 533M record leaked.

### 11.4 Difese

- **Inventory completo** delle API (OpenAPI spec di tutte, no eccezioni)
- **Versioning chiaro** + deprecation policy
- **API Gateway** centralizzato (Kong, Apigee, AWS API Gateway)
- **Network segmentation**: staging/dev mai esposti su Internet
- **Discovery scanning** con tool (es. Kiterunner, Burp Discovery)

---

<a name="cap12"></a>
## 12. API10 — Unsafe Consumption of APIs

### 12.1 Cos'è

L'app **chiama API di terzi** (Stripe, Twilio, Google) e si fida ciecamente delle risposte.

### 12.2 Rischi

- **Risposta manipolata in transit** → senza TLS = MITM
- **API terza compromessa** → restituisce payload malevolo
- **Webhook senza firma**: chiunque può chiamare il tuo endpoint webhook fingendosi Stripe

### 12.3 Esempio webhook insicuro

```python
# 🚩 VULNERABILE
@app.post("/webhook/stripe")
def stripe_webhook():
    event = request.json
    if event["type"] == "payment_intent.succeeded":
        mark_paid(event["data"]["object"]["id"])
    return "ok"
```

Attaccante chiama il webhook fingendo un pagamento. **Ordine pagato senza pagare nulla**.

### 12.4 Difesa — verifica firma webhook

```python
import stripe
endpoint_secret = "whsec_..."

@app.post("/webhook/stripe")
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError:
        abort(400)

    if event["type"] == "payment_intent.succeeded":
        mark_paid(event["data"]["object"]["id"])
    return "ok"
```

Stripe firma ogni webhook con HMAC. Solo chi conosce il `endpoint_secret` può forgiare un evento valido.

### 12.5 Altri pattern

- TLS sempre per API esterne (e validare cert).
- Timeout aggressivi.
- Schema validation della risposta.
- Circuit breaker (se API esterna down, non bloccare).

---

<a name="cap13"></a>
## 13. Lab pratico — FastAPI con difese

### 13.1 Setup

```bash
pip install fastapi uvicorn pydantic[email] python-jose[cryptography] passlib[bcrypt] slowapi
```

### 13.2 Codice

```python
# api_secure.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field
from jose import jwt, JWTError
from slowapi import Limiter
from slowapi.util import get_remote_address
import time

SECRET = "uno-secret-lungo-e-random"
ALGO = "HS256"

app = FastAPI(title="Secure API Demo")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Mock DB
USERS = {
    "alice": {"id": 1, "password": "alice123", "role": "user"},
    "admin": {"id": 2, "password": "admin123", "role": "admin"},
}
ORDERS = [
    {"id": 100, "user_id": 1, "amount": 50.0, "secret_internal_score": 75},
    {"id": 101, "user_id": 2, "amount": 200.0, "secret_internal_score": 99},
]


# === PYDANTIC MODELS ===
class UserPublic(BaseModel):
    id: int
    username: str
    role: str

class OrderPublic(BaseModel):
    """Response model: NON include secret_internal_score"""
    id: int
    user_id: int
    amount: float

class OrderUpdate(BaseModel):
    """Request model: solo amount modificabile"""
    amount: float = Field(gt=0, le=1_000_000)


# === AUTH ===
def make_token(username: str, role: str) -> str:
    return jwt.encode({
        "sub": username, "role": role,
        "iat": int(time.time()), "exp": int(time.time()) + 900,
        "iss": "myapi", "aud": "myclients"
    }, SECRET, algorithm=ALGO)


def current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO],
                             audience="myclients", issuer="myapi")
    except JWTError:
        raise HTTPException(401, "invalid token")
    user = USERS.get(payload["sub"])
    if not user:
        raise HTTPException(401, "user not found")
    return {"username": payload["sub"], **user}


def require_admin(user=Depends(current_user)):
    if user["role"] != "admin":
        raise HTTPException(403, "admin only")
    return user


# === ENDPOINTS ===
@app.post("/login")
@limiter.limit("5/minute")              # API4: rate limit
async def login(request: Request,
                username: str, password: str):
    u = USERS.get(username)
    if not u or u["password"] != password:
        raise HTTPException(401, "invalid credentials")
    return {"access_token": make_token(username, u["role"]),
            "token_type": "bearer"}


@app.get("/me", response_model=UserPublic)
def me(user=Depends(current_user)):
    return UserPublic(id=user["id"], username=user["username"], role=user["role"])


@app.get("/orders", response_model=list[OrderPublic])
def my_orders(user=Depends(current_user)):
    # API1: nessun BOLA — filtra per user del token
    return [OrderPublic(**o) for o in ORDERS if o["user_id"] == user["id"]]


@app.get("/orders/{oid}", response_model=OrderPublic)
def get_order(oid: int, user=Depends(current_user)):
    o = next((o for o in ORDERS if o["id"] == oid), None)
    if not o:
        raise HTTPException(404)
    if o["user_id"] != user["id"] and user["role"] != "admin":
        raise HTTPException(403)        # API1: ownership check
    return OrderPublic(**o)


@app.put("/orders/{oid}", response_model=OrderPublic)
def update_order(oid: int, payload: OrderUpdate, user=Depends(current_user)):
    o = next((o for o in ORDERS if o["id"] == oid), None)
    if not o or o["user_id"] != user["id"]:
        raise HTTPException(403)
    o["amount"] = payload.amount       # API3: solo `amount` modificabile
    return OrderPublic(**o)


@app.get("/admin/orders", response_model=list[OrderPublic])
def all_orders(_=Depends(require_admin)):
    # API5: function level authz
    return [OrderPublic(**o) for o in ORDERS]
```

### 13.3 Avvio

```bash
uvicorn api_secure:app --reload
```

### 13.4 Test

Visita `http://localhost:8000/docs` (Swagger UI generato automaticamente).

```bash
# Login
TOKEN=$(curl -X POST http://localhost:8000/login \
  -d "username=alice&password=alice123" | jq -r .access_token)

# Lista ordini (vedo solo i miei, anche se ne esistono altri)
curl http://localhost:8000/orders -H "Authorization: Bearer $TOKEN"

# Tento BOLA — leggo ordine #101 (di admin)
curl http://localhost:8000/orders/101 -H "Authorization: Bearer $TOKEN"
# → 403

# Tento BOPLA — provo a impostare campo non in OrderUpdate
curl -X PUT http://localhost:8000/orders/100 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "secret_internal_score": 999}'
# → secret_internal_score IGNORATO (Pydantic strict)

# Tento function-level — chiamo /admin/orders come alice
curl http://localhost:8000/admin/orders -H "Authorization: Bearer $TOKEN"
# → 403 admin only
```

---

<a name="cap14"></a>
## 14. Checklist API Security

### 14.1 Per ogni endpoint

- [ ] Autenticazione richiesta? (default: sì, eccezione: /login, /health)
- [ ] Autorizzazione su oggetto (BOLA)
- [ ] Autorizzazione su funzione (admin endpoint)
- [ ] Response model con whitelist campi (BOPLA)
- [ ] Request model con whitelist campi (Mass assignment)
- [ ] Rate limit
- [ ] Pagination su list endpoint
- [ ] Validation input (Pydantic)
- [ ] Error handler che non rivela stack trace

### 14.2 Architettura

- [ ] OpenAPI spec aggiornata e completa
- [ ] API gateway davanti (es. Kong)
- [ ] Versioning chiaro (`/v1/`, `/v2/`)
- [ ] Deprecation policy + sunset notification
- [ ] Network segmentation (no metadata cloud accessible)
- [ ] CORS con origin whitelist
- [ ] HTTPS forzato + HSTS

### 14.3 Logging & monitoring

- [ ] Log di ogni 4xx/5xx con context (user, endpoint, IP)
- [ ] Alert su pattern (es. >10 BOLA tentativi/min)
- [ ] Alert su login falliti pattern
- [ ] WAF/anti-bot per flussi critici

---

## Per approfondire

- **OWASP API Security Top 10 (2023)**: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- **PortSwigger Academy — API Testing**: https://portswigger.net/web-security/api-testing
- **42Crunch API Security Whitepapers**: https://42crunch.com
- **Kong/Apigee/AWS API Gateway**: documenti vendor

---

> **Suggerimento di integrazione**:
> - Lettura tra G7-G8 del corso 32h
> - Lab opzionale di 2h dopo M6
> - Capitolo principale di un eventuale "Modulo Avanzato API"
