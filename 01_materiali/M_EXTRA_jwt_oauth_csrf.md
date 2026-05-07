# EXTRA — JWT, OAuth 2.0, SSO, CSRF approfondito

**Materiale integrativo — Corso ITS Cybersecurity**
**Tipologia**: estensione di M3 (HTTP) e M6.4 (autenticazione)
**Tempo suggerito**: 3-4 ore (lettura + lab)
**Prerequisiti**: M3 (HTTP, cookie), M6.4 (password hashing)

> Questo materiale colma una lacuna del corso base: l'autenticazione **moderna** non si fa più solo con cookie di sessione. JWT, OAuth 2.0, OIDC e SSO sono lo standard de facto in ogni azienda. Un developer che entra in azienda nel 2026 senza saperli è in difficoltà al primo giorno.

---

## Indice

- [1. Cookie session vs JWT vs OAuth — la mappa](#cap1)
- [2. JWT — JSON Web Token](#cap2)
- [3. Vulnerabilità JWT (e come bucarli)](#cap3)
- [4. OAuth 2.0 — il protocollo](#cap4)
- [5. OpenID Connect (OIDC)](#cap5)
- [6. SSO — Single Sign-On](#cap6)
- [7. Refresh token & token rotation](#cap7)
- [8. CSRF approfondito](#cap8)
- [9. Lab pratico — JWT + Flask](#cap9)
- [10. Checklist & antipattern](#cap10)

---

<a name="cap1"></a>
## 1. Cookie session vs JWT vs OAuth — la mappa

| Approccio | Stato dove | Use case | Complessità |
|-----------|-----------|----------|-------------|
| **Cookie session** | Server (DB sessions) | Webapp tradizionale monolitica | Bassa |
| **JWT** | Client (token firmato) | API stateless, microservizi, SPA | Media |
| **OAuth 2.0** | Server (auth server) | Login con Google/GitHub/SSO | Alta |
| **OIDC** | Server + ID token | OAuth + identità | Alta |
| **SAML** | Browser-mediated | SSO enterprise legacy | Molto alta |

> **Regola pratica**: se hai una webapp tradizionale + DB → cookie session è ancora ottimo. Se hai mobile + SPA + 5 microservizi → JWT/OAuth.

### 1.1 Quando usare cosa

- **Cookie session**: Flask, Rails, Django classici. Server-side rendering. Login interno.
- **JWT**: API REST/GraphQL consumate da SPA o mobile. Stateless. Microservizi che devono validare il token senza chiamare un auth server centralizzato ad ogni request.
- **OAuth 2.0**: "Login con Google", "Connect with GitHub", access delegato a Drive/Calendar.
- **OIDC**: come OAuth ma con identità verificabile (chi è l'utente, non solo cosa può fare).
- **SAML**: SSO aziendale (Okta, Active Directory Federation Services). XML-based, enterprise.

---

<a name="cap2"></a>
## 2. JWT — JSON Web Token

> RFC 7519. Pronunciato "jot".

### 2.1 Struttura

Un JWT è una stringa di **3 parti separate da punto**:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NSIsImV4cCI6MTcxOTM2MDAwMH0.4eK7vK_xGr6Kr9wXnQzQ9kZJWvVQz7iH8...
   └────────── HEADER ─────────────┘ └─────────── PAYLOAD ───────────┘ └────── SIGNATURE ──────┘
```

Tutto **Base64URL-encoded**.

### 2.2 Header

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

- `alg`: algoritmo di firma (HS256, RS256, ES256, **none** ⚠️)
- `typ`: tipo (sempre "JWT")

### 2.3 Payload (Claims)

```json
{
  "sub": "user_id_12345",
  "name": "Mario Rossi",
  "iat": 1719356400,
  "exp": 1719360000,
  "roles": ["user", "admin"]
}
```

**Claims standard (RFC 7519)**:

| Claim | Significato |
|-------|-------------|
| `iss` | Issuer (chi ha emesso il token) |
| `sub` | Subject (chi è l'utente) |
| `aud` | Audience (per quale servizio) |
| `exp` | Expiration time (Unix timestamp) |
| `nbf` | Not before |
| `iat` | Issued at |
| `jti` | JWT ID (univoco per revoke) |

**Custom claims**: puoi metterci quello che vuoi (`roles`, `tenant_id`, ecc.).

⚠️ **Il payload non è cifrato, è Base64**. Chiunque può leggerlo. Non metterci dati sensibili.

### 2.4 Signature

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  SECRET_KEY
)
```

Con **HS256**: firma simmetrica con chiave segreta condivisa.
Con **RS256**: firma asimmetrica con chiave privata; il client verifica con la pubblica.

### 2.5 Esempio Python

```python
import jwt   # pip install pyjwt

SECRET = "uno-segreto-lungo-e-random-non-questo"

# Generare un token
token = jwt.encode(
    {
        "sub": "user_12345",
        "exp": int(time.time()) + 3600,  # 1 ora
        "roles": ["user"],
    },
    SECRET,
    algorithm="HS256"
)

# Verificare
try:
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    print(payload)
except jwt.ExpiredSignatureError:
    print("Token scaduto")
except jwt.InvalidTokenError:
    print("Token invalido")
```

### 2.6 Vantaggi e svantaggi

**Vantaggi**:
- ✅ Stateless (nessuna sessione DB)
- ✅ Funziona cross-domain
- ✅ Standard universale
- ✅ Ottimo per microservizi (ogni servizio verifica indipendentemente)

**Svantaggi**:
- ❌ Non puoi "invalidarli" facilmente (devi mantenere blacklist o usare token brevi)
- ❌ Se compromessi, validi fino a scadenza
- ❌ Payload visibile (no dati sensibili)
- ❌ Implementazione errata = vulnerabilità grave

---

<a name="cap3"></a>
## 3. Vulnerabilità JWT (e come bucarli)

### 3.1 Algorithm: none

L'attacco più famoso. RFC 7519 prevede `alg: none` per token "non firmati". **Pessima idea.**

```json
// Header malevolo
{
  "alg": "none",
  "typ": "JWT"
}
```

Token: `BASE64(header).BASE64(payload).` (signature vuota)

**Difesa**:
```python
# ❌ VULNERABILE — non specifica algoritmi
jwt.decode(token, SECRET)

# ✅ SICURO — whitelist algoritmi
jwt.decode(token, SECRET, algorithms=["HS256"])
```

### 3.2 Algorithm confusion (HS256 ↔ RS256)

Un'app verifica con `RS256` usando chiave **pubblica**. Attaccante:
1. Cambia `alg` in `HS256`.
2. Firma il token con la **chiave pubblica** (che è... pubblica).
3. Server verifica con stessa chiave pubblica come HS256 → valido.

**Difesa**: forzare l'algoritmo lato server, mai accettare quello del header.

### 3.3 Secret debole

```python
SECRET = "secret"
SECRET = "12345"
SECRET = "password"
```

Brute-force con `hashcat` su HS256 → secret trovato in minuti.

**Difesa**: generare secret con `secrets.token_urlsafe(64)` o usare RS256 con chiave 2048+ bit.

### 3.4 Token senza scadenza

```json
// Token "vita eterna"
{
  "sub": "user",
  "roles": ["admin"]
}
```

Se compromesso → attaccante ha accesso indefinito.

**Difesa**: `exp` sempre, idealmente <1 ora per access token.

### 3.5 Nessun controllo `aud`/`iss`

Un token rilasciato da `auth.example.com` per `api.example.com` non dovrebbe funzionare su `api.altro.com`. Senza check di `aud`/`iss`, sì.

**Difesa**:
```python
jwt.decode(token, SECRET, algorithms=["HS256"],
           audience="api.example.com",
           issuer="auth.example.com")
```

### 3.6 JWT salvati in localStorage

Pattern frequente: SPA salva JWT in `localStorage`. **XSS = furto JWT**.

**Soluzione corretta**:
- JWT in **cookie HttpOnly + Secure + SameSite=Strict**.
- Per le richieste SPA: cookie inviato automaticamente dal browser.
- CSRF mitigato con SameSite o token CSRF separato.

### 3.7 Tabella riassuntiva

| Vulnerabilità | Difesa |
|---------------|--------|
| `alg: none` | Whitelist algoritmi |
| Algorithm confusion | Forzare algoritmo |
| Secret debole | `token_urlsafe(64)` o RS256 |
| No expiration | `exp` < 1 ora |
| No audience/issuer check | `aud`/`iss` validation |
| Storage in localStorage | Cookie HttpOnly |

---

<a name="cap4"></a>
## 4. OAuth 2.0 — il protocollo

> RFC 6749. Standard per **accesso delegato**.

### 4.1 Il problema che risolve

> "Voglio dare a Calendar.app accesso al mio Google Calendar, **senza dargli la mia password Google**."

Pre-OAuth: condividevi la password (era così, scioccante a pensarci).
Post-OAuth: Google emette un **token** che Calendar.app può usare per il calendario, niente altro, e revocabile.

### 4.2 I 4 ruoli

1. **Resource Owner**: l'utente (tu).
2. **Client**: l'app che richiede accesso (Calendar.app).
3. **Authorization Server**: chi emette token (Google).
4. **Resource Server**: chi possiede i dati (Google Calendar API).

### 4.3 Il flow più comune — Authorization Code (con PKCE)

```
┌─────────┐                                            ┌──────────────┐
│ Utente  │                                            │ Auth Server  │
│ (Browser)│                                           │   (Google)   │
└────┬────┘                                            └──────┬───────┘
     │ 1. Click "Login with Google"                           │
     ├──── redirect ────────────────────────────────────────►│
     │                                                        │
     │ 2. Login + consent ("Calendar.app vuole accesso a...") │
     ◄────────────────────────────────────────────────────────┤
     │                                                        │
     │ 3. Approvo → redirect a Calendar.app con CODE          │
     ├────────────────────────►┌──────────────────┐           │
     │                          │  Calendar.app    │           │
     │                          │     (Client)     │           │
     │                          └────────┬─────────┘           │
     │                                   │ 4. Scambia CODE     │
     │                                   │    + verifier       │
     │                                   ├────────────────────►│
     │                                   │                     │
     │                                   │ 5. ACCESS TOKEN     │
     │                                   ◄─────────────────────┤
     │                                   │                     │
     │                          ┌────────▼─────────┐           │
     │                          │ API Calendar     │           │
     │                          │ Authorization:   │           │
     │                          │   Bearer eyJ...  │           │
     │                          └──────────────────┘           │
```

### 4.4 PKCE (Proof Key for Code Exchange)

Esteensione obbligatoria per app pubbliche (mobile, SPA). Difende da intercettazione del code:

1. Client genera `code_verifier` (random).
2. Client calcola `code_challenge = SHA256(code_verifier)`.
3. Manda `code_challenge` nella richiesta authorization.
4. Quando scambia il code per il token, manda anche `code_verifier`.
5. Server verifica `SHA256(code_verifier) == code_challenge`.

> **Difesa**: anche se attaccante intercetta il code, senza il `code_verifier` originale non può scambiarlo.

### 4.5 Altri grant types (cenni)

| Grant | Quando usare | Sicurezza |
|-------|--------------|-----------|
| Authorization Code + PKCE | App pubblica (mobile, SPA) | ✅ Standard moderno |
| Authorization Code | Backend con secret | ✅ OK |
| Client Credentials | Service-to-service | ✅ OK |
| Resource Owner Password | Legacy (sconsigliato) | ❌ Deprecato |
| Implicit | Legacy SPA | ❌ Deprecato (sostituito da Code+PKCE) |

### 4.6 Vulnerabilità OAuth comuni

- **Open redirect**: `redirect_uri` non validata → token rubato.
- **CSRF su authorization request**: usare `state` parameter sempre.
- **Code interception**: usare PKCE.
- **Token leakage in logs/Referer**: usare `Authorization: Bearer`, non query string.

---

<a name="cap5"></a>
## 5. OpenID Connect (OIDC)

> Layer di **identità** sopra OAuth 2.0.

### 5.1 Differenza con OAuth puro

- **OAuth 2.0** dice "questo token può fare X".
- **OIDC** dice "questo token può fare X **e l'utente è Y**".

OIDC aggiunge un **ID Token** (un JWT) con claims sull'utente: `sub`, `email`, `name`, `picture`.

### 5.2 ID Token vs Access Token

| | ID Token | Access Token |
|---|----------|--------------|
| Per chi? | Client (app) | Resource Server (API) |
| Cosa contiene | Identità utente | Permessi |
| Formato | Sempre JWT | Spesso JWT, può essere opaque |
| Validato da | Client (verifica firma) | API |

### 5.3 Esempio Python con `authlib`

```python
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@app.route("/login")
def login():
    return oauth.google.authorize_redirect(url_for("auth_callback", _external=True))

@app.route("/auth/callback")
def auth_callback():
    token = oauth.google.authorize_access_token()
    userinfo = token["userinfo"]
    # userinfo = {"sub": "...", "email": "...", "name": "..."}
    session["user"] = userinfo
    return redirect("/dashboard")
```

`server_metadata_url` è il **discovery endpoint** OIDC: scarica automaticamente endpoint, chiavi pubbliche, algoritmi supportati.

---

<a name="cap6"></a>
## 6. SSO — Single Sign-On

> Login una volta, accesso a N applicazioni.

### 6.1 Approcci SSO

- **OIDC SSO** (moderno): login centrale via OIDC, ogni app riceve l'ID token. Standard nuovo.
- **SAML 2.0** (enterprise): XML-based, vecchio ma diffuso. Active Directory, Okta, OneLogin.
- **Kerberos** (intranet aziendali): Windows AD interno.

### 6.2 SAML in 30 secondi

```
Utente → SP (Service Provider, es. SalesForce)
       ← redirect a IdP (Identity Provider, es. Okta)
Utente → IdP login
       ← SAML Assertion (XML firmato) tornata al SP via browser POST
SP verifica firma → utente loggato
```

> Se devi integrare SAML: usa una libreria. Mai parser XML manuale (XXE, XSW attacks).

### 6.3 IdP popolari

- **Okta** (enterprise, comune in USA)
- **Auth0** (developer-friendly, ora di Okta)
- **Microsoft Entra ID** (ex Azure AD, enterprise + cloud)
- **Google Workspace**
- **Keycloak** (open source, self-hosted)
- **Authentik** (open source moderno)

### 6.4 Quando NON fare SSO custom

> **Sempre.** Usa un IdP gestito o una libreria provata. SSO custom = bug di sicurezza assicurati.

---

<a name="cap7"></a>
## 7. Refresh token & token rotation

### 7.1 Il problema dei JWT brevi

Per sicurezza vuoi access token brevi (15-30 min). Ma chiedere login ogni 15 min è UX terribile.

### 7.2 Soluzione: refresh token

- **Access token**: breve (15-30 min). JWT. Mandato in `Authorization: Bearer`.
- **Refresh token**: lungo (7-30 giorni). **Opaco** (random). In cookie HttpOnly.
- Quando access scade, client usa refresh per ottenere uno nuovo, **senza login utente**.

### 7.3 Refresh token rotation

Pattern moderno:

1. Client usa `refresh_token_v1` per ottenere nuovo access token.
2. Server emette nuovo access **e** nuovo `refresh_token_v2`.
3. `refresh_token_v1` viene **invalidato**.

**Vantaggio**: se attaccante ruba `refresh_token_v1` e tu lo usi prima → server invalida tutta la catena, l'attaccante perde l'accesso.

### 7.4 Refresh token reuse detection

Se `refresh_token_v1` viene presentato **due volte**, è probabile un attacco (qualcuno l'ha rubato e ne sta fasando di un'altra rotation).

**Difesa**: revocare l'intera famiglia di refresh token e forzare login.

### 7.5 Esempio architettura

```
Login →  AS rilascia:
         - access_token  (JWT, 15 min)
         - refresh_token (UUID, 7 giorni, salvato in DB con famiglia + status)

Ogni 15 min → client chiama /refresh con refresh_token
              ↓
         AS verifica:
         - refresh_token esiste in DB? Status = ACTIVE?
         - Se sì: emetti nuovo access_token + nuovo refresh_token
                  invalida vecchio refresh_token (status=USED)
         - Se no (es. status=USED): REVOKE FAMILY (alert!)
                  forza login utente.
```

---

<a name="cap8"></a>
## 8. CSRF approfondito

> Trattato nel corso base solo come "cenno" via SameSite. Qui il dettaglio completo.

### 8.1 Cos'è CSRF

L'attaccante fa eseguire **al browser della vittima** una richiesta verso un sito su cui è già loggata, **senza che la vittima lo sappia**.

### 8.2 Esempio classico — pre-SameSite

Utente loggato su `bank.com`. Visita `evil.com`. La pagina di evil contiene:

```html
<form action="https://bank.com/transfer" method="POST">
  <input type="hidden" name="to" value="attacker_account">
  <input type="hidden" name="amount" value="10000">
</form>
<script>document.forms[0].submit();</script>
```

Browser invia la POST con il **cookie di sessione** di bank.com (perché è automatico) → **bonifico eseguito**.

### 8.3 Le 4 difese contro CSRF

#### A. **SameSite cookie** (default moderno, GOLD)

```
Set-Cookie: session=abc; SameSite=Lax; Secure; HttpOnly
```

- `Lax` (default browser moderni): cookie inviato in navigazione top-level (click), NON in form auto-submit cross-site.
- `Strict`: mai cross-site, anche con click. UX a volte rotta.
- `None`: sempre. Richiede `Secure`. Solo se davvero serve cross-site (es. SSO).

> Coperto **automaticamente** la maggior parte dei CSRF moderni. Da solo non basta — sempre **A + B** insieme.

#### B. **CSRF token** (Synchronizer Token Pattern)

```html
<form method="POST">
  <input type="hidden" name="csrf_token" value="r4ndomG3n3rato5erverSide">
  ...
</form>
```

Server valida che `csrf_token` nel form == quello in sessione. Attaccante non può prevederlo.

In **Flask** con `Flask-WTF`:

```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# Nei template:
# {{ csrf_token() }}
```

#### C. **Double-submit cookie** (per API)

- Server emette cookie `csrf_cookie = X` (NON HttpOnly).
- Client legge il cookie e lo manda anche come header `X-CSRF-Token: X`.
- Server verifica che siano uguali.

Funziona perché:
- Browser invia automaticamente il cookie (anche cross-site).
- JS di evil.com **non può leggere** il cookie di bank.com (Same-Origin Policy) → non può aggiungere il header.

#### D. **Custom request header**

```javascript
fetch("/api/transfer", {
  method: "POST",
  headers: {"X-Requested-With": "XMLHttpRequest"},
  ...
})
```

Server verifica presenza del header. Browser blocca cross-site requests con header custom (CORS preflight).

> Solo per API JSON, non per form HTML normali.

### 8.4 Quando CSRF NON si applica

- Endpoint che restituiscono solo dati (no side effects): GET safe.
- Endpoint con **autenticazione via header** (Bearer token in JS) e **non via cookie**: l'attaccante non può aggiungere il header → no CSRF.

### 8.5 Errori comuni

- ❌ Solo CSRF token, senza SameSite (manca difesa in profondità).
- ❌ Solo SameSite, senza CSRF token (alcuni browser legacy ancora in giro).
- ❌ CSRF token valido per sempre (deve scadere o essere per-request).
- ❌ CSRF token nel **GET URL** (finisce nei log Referer, ecc.).

---

<a name="cap9"></a>
## 9. Lab pratico — JWT + Flask

### 9.1 Setup

```bash
pip install flask pyjwt python-dotenv
```

### 9.2 Codice: app.py

```python
import time, os, secrets
from functools import wraps
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
SECRET = os.getenv("JWT_SECRET", secrets.token_urlsafe(64))
ALGO = "HS256"
TTL_ACCESS = 15 * 60        # 15 min
TTL_REFRESH = 7 * 24 * 3600 # 7 giorni

# Mock DB utenti (in produzione: PostgreSQL + bcrypt)
USERS = {
    "alice": {"password": "alice123", "roles": ["user"]},
    "admin": {"password": "admin123", "roles": ["user", "admin"]},
}

# Mock DB refresh tokens (in produzione: Redis o DB)
REFRESH_DB = {}  # token_id -> {"user": ..., "status": "ACTIVE/USED/REVOKED", "family": ...}


def make_access_token(user: str, roles: list):
    payload = {
        "sub": user,
        "roles": roles,
        "iss": "myapp",
        "aud": "myapi",
        "iat": int(time.time()),
        "exp": int(time.time()) + TTL_ACCESS,
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)


def make_refresh_token(user: str, family: str = None):
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
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "missing token"}), 401
        token = auth[7:]
        try:
            payload = jwt.decode(token, SECRET, algorithms=[ALGO],
                                 audience="myapi", issuer="myapp")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid token"}), 401
        request.user = payload
        return f(*args, **kwargs)
    return wrapper


def require_role(role: str):
    def deco(f):
        @wraps(f)
        @require_jwt
        def wrapper(*args, **kwargs):
            if role not in request.user.get("roles", []):
                return jsonify({"error": "forbidden"}), 403
            return f(*args, **kwargs)
        return wrapper
    return deco


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    user = data.get("username", "")
    pwd = data.get("password", "")
    u = USERS.get(user)
    # In produzione: bcrypt.checkpw
    if not u or u["password"] != pwd:
        return jsonify({"error": "invalid credentials"}), 401

    access = make_access_token(user, u["roles"])
    refresh, family = make_refresh_token(user)
    return jsonify({"access_token": access, "refresh_token": refresh})


@app.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json() or {}
    rt = data.get("refresh_token", "")
    rec = REFRESH_DB.get(rt)
    if not rec:
        return jsonify({"error": "invalid refresh"}), 401

    if rec["status"] != "ACTIVE":
        # Reuse detection! Revoke whole family.
        for tid, r in REFRESH_DB.items():
            if r.get("family") == rec.get("family"):
                r["status"] = "REVOKED"
        return jsonify({"error": "token reuse detected — login again"}), 401

    if time.time() > rec["exp"]:
        return jsonify({"error": "refresh expired"}), 401

    # Rotation: invalida vecchio, emetti nuovo
    rec["status"] = "USED"
    user = rec["user"]
    new_access = make_access_token(user, USERS[user]["roles"])
    new_refresh, _ = make_refresh_token(user, family=rec["family"])
    return jsonify({"access_token": new_access, "refresh_token": new_refresh})


@app.route("/me")
@require_jwt
def me():
    return jsonify({"user": request.user["sub"], "roles": request.user["roles"]})


@app.route("/admin")
@require_role("admin")
def admin():
    return jsonify({"secret": "admin-only data"})


if __name__ == "__main__":
    app.run(debug=True)
```

### 9.3 Test (curl)

```bash
# Login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"alice123"}'

# Risposta:
# {"access_token":"eyJ...","refresh_token":"abc..."}

# Test endpoint protetto
curl http://localhost:5000/me \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Refresh
curl -X POST http://localhost:5000/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<REFRESH_TOKEN>"}'

# Test admin (solo se ti sei loggato come "admin")
curl http://localhost:5000/admin \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 9.4 Esercizi

1. **Algorithm none attack**: prova a forgiare un token con `alg: none` e mandalo. Cosa succede? (Spoiler: pyjwt rifiuta perché whitelist algoritmi.)
2. **Token expiration**: aspetta 16 minuti, riprova `/me`. Errore atteso?
3. **Refresh reuse**: usa lo stesso refresh token due volte. Cosa restituisce la seconda chiamata?
4. **Estendi**: aggiungi endpoint `/logout` che invalida il refresh token.
5. **JWT in cookie HttpOnly**: invece di restituire access in JSON, mettilo in cookie HttpOnly + Secure + SameSite=Lax. Quale endpoint cambia?

---

<a name="cap10"></a>
## 10. Checklist & antipattern

### 10.1 Checklist JWT/OAuth

- [ ] `algorithms=["HS256"]` (o RS256) **whitelist** in decode
- [ ] Mai `alg: none` accettato
- [ ] Secret >= 256 bit, generato con CSPRNG
- [ ] `exp` sempre, < 1 ora per access token
- [ ] `aud` e `iss` validati
- [ ] Refresh token con rotation
- [ ] Refresh reuse detection
- [ ] JWT in cookie HttpOnly se è una webapp (non in localStorage)
- [ ] Logout invalida refresh token nel DB
- [ ] Per OAuth: `state` parameter sempre (anti-CSRF)
- [ ] Per OAuth pubblico: PKCE obbligatorio
- [ ] `redirect_uri` whitelist (no open redirect)

### 10.2 Checklist CSRF

- [ ] `SameSite=Lax` o `Strict` su cookie di sessione
- [ ] CSRF token su tutti i POST/PUT/DELETE form-based
- [ ] Token CSRF per-request (non globale)
- [ ] Token CSRF NON nel GET URL
- [ ] Per API JSON: header custom (`X-Requested-With`) o double-submit
- [ ] Per state-changing: solo POST/PUT/DELETE (mai GET)

### 10.3 Antipattern frequenti

| Antipattern | Conseguenza |
|-------------|-------------|
| JWT in localStorage | XSS = furto token |
| Access token "vita eterna" | Compromesso = accesso illimitato |
| Stesso JWT per tutto (no audience) | Token rilasciato per X usato su Y |
| Refresh token senza rotation | Reuse non rilevato |
| OAuth senza `state` | CSRF su login |
| OAuth `redirect_uri` aperto | Token redirect a evil.com |
| CSRF token globale | Riusabile, perde valore |
| Auth solo lato client | Bypass banale |
| `eval()` su payload JWT | RCE |

---

## Per approfondire

- **PortSwigger Academy — JWT Authentication**: https://portswigger.net/web-security/jwt
- **OAuth 2.0 Simplified** (Aaron Parecki): https://www.oauth.com
- **OWASP JWT Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
- **OWASP CSRF Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
- **NIST Digital Identity Guidelines** (SP 800-63): https://pages.nist.gov/800-63-3/

---

> **Suggerimento di integrazione nel corso 32h**:
> Questo materiale può essere usato come:
> - **Lettura** assegnata tra G6 e G7
> - **Lab opzionale** in M3 (1h aggiuntiva)
> - **Capitolo** del corso "32h Avanzato" di II anno
