---
title: "EXTRA — JWT, OAuth 2.0, SSO, CSRF"
subtitle: "Corso ITS Cybersecurity — Modulo Avanzato"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# EXTRA — JWT, OAuth 2.0, CSRF
## 3-4 ore — Autenticazione moderna

## Obiettivi

- Cookie session vs JWT vs OAuth — quando usare cosa
- JWT struttura, vulnerabilità, difese
- OAuth 2.0 + PKCE
- OpenID Connect, SSO
- Refresh token rotation
- CSRF approfondito (3 difese in profondità)

## Cookie session vs JWT vs OAuth

| | Stato | Use case |
|---|-------|----------|
| **Cookie session** | Server (DB) | Webapp tradizionale |
| **JWT** | Client (firmato) | API, SPA, microservizi |
| **OAuth 2.0** | Auth server | Login con Google/GitHub |
| **OIDC** | Auth server + ID | OAuth + identità |
| **SAML** | Browser-mediated | SSO enterprise legacy |

## JWT — struttura

```
HEADER.PAYLOAD.SIGNATURE
   ↓        ↓        ↓
 alg     claims    HMAC/RSA
```

Tutto **Base64URL-encoded**. Il payload **non è cifrato**, è leggibile. Solo **firmato**.

## JWT — Header

```json
{ "alg": "HS256", "typ": "JWT" }
```

- `alg`: HS256 (simmetrico) o RS256 (asimmetrico)
- ⚠️ **mai accettare `alg: none`**

## JWT — Payload (claims)

```json
{
  "sub": "user_12345",
  "iat": 1719356400,
  "exp": 1719360000,
  "aud": "myapi",
  "iss": "myauth",
  "roles": ["user"]
}
```

`exp`, `aud`, `iss` **sempre** validati lato server.

## JWT — Signature

```
HMACSHA256(
  base64(header) + "." + base64(payload),
  SECRET
)
```

> Modifica payload → firma cambia → server rigetta.

## JWT in Python

```python
import jwt
SECRET = "uno-secret-lungo-CSPRNG"

# Generare
token = jwt.encode({
    "sub": "user_id", "exp": time.time() + 900,
    "iss": "myapi", "aud": "myclients"
}, SECRET, algorithm="HS256")

# Verificare (whitelist algoritmo!)
payload = jwt.decode(token, SECRET,
                     algorithms=["HS256"],
                     audience="myclients", issuer="myapi")
```

## Vulnerabilità JWT — alg: none

```python
# 🚩 VULNERABILE
jwt.decode(token, SECRET)   # accetta qualsiasi alg

# ✅ SICURO
jwt.decode(token, SECRET, algorithms=["HS256"])
```

L'attaccante manda `alg: none` con firma vuota → token "valido".

## Vulnerabilità — Algorithm confusion

App verifica con RS256 (chiave pubblica).
Attaccante:
1. Cambia `alg` in HS256
2. Firma con la chiave **pubblica** (è pubblica)
3. Server verifica con stessa chiave → valido

> Difesa: forzare algoritmo, mai dal header.

## Vulnerabilità — secret debole

```python
SECRET = "secret"     # 🔥
SECRET = "12345"      # 🔥
SECRET = "password"   # 🔥
```

Hashcat brute-force HS256 → secret in minuti.

```python
# ✅
import secrets
SECRET = secrets.token_urlsafe(64)
```

## Vulnerabilità — no expiration / no aud

- Token "vita eterna" → compromesso = accesso illimitato
- Token rilasciato per `api.X` accettato da `api.Y`

> Sempre `exp < 1h` + `aud` + `iss` validati.

## Vulnerabilità — JWT in localStorage

```javascript
// 🚩 SPA classica
localStorage.setItem("token", jwt);
fetch("/api", {headers: {Authorization: `Bearer ${jwt}`}});
```

XSS = furto token.

> ✅ JWT in cookie HttpOnly + Secure + SameSite

## OAuth 2.0 — il problema

> "Voglio dare a Calendar.app accesso al mio Google Calendar **senza dargli la mia password Google**"

Pre-OAuth: condividevi la password.
Post-OAuth: token scoped + revocabile.

## OAuth 2.0 — i 4 ruoli

1. **Resource Owner** = utente
2. **Client** = app che richiede accesso
3. **Authorization Server** = chi emette token (Google)
4. **Resource Server** = chi possiede i dati (Google API)

## Authorization Code Flow + PKCE

```
Utente → click "Login con X"
       ← redirect ad Auth Server
Utente → consent
       → redirect a Client con CODE
Client → scambia CODE+verifier per ACCESS TOKEN
       → usa token su Resource Server
```

## PKCE — Proof Key for Code Exchange

Estensione obbligatoria per app pubbliche (mobile, SPA).

1. Client genera `code_verifier` (random)
2. `code_challenge = SHA256(verifier)`
3. Auth request include challenge
4. Token request include verifier
5. Server verifica match

> Anche se attaccante intercetta il code, senza verifier non può scambiarlo.

## OAuth — vulnerabilità comuni

- **Open redirect** sul `redirect_uri` non validato
- **CSRF** su authorization request → usa `state`
- **Code interception** → usa PKCE
- **Token in query string** → finisce nei log/Referer

## OpenID Connect (OIDC)

- OAuth 2.0 dice "questo token può fare X"
- OIDC dice "+ l'utente è Y"

OIDC aggiunge **ID Token** (JWT con identità).

| | ID Token | Access Token |
|---|----------|--------------|
| Per chi | Client | API |
| Cosa contiene | Identità | Permessi |
| Formato | JWT | Spesso JWT |

## OIDC con authlib

```python
from authlib.integrations.flask_client import OAuth

oauth.register(
    name="google",
    client_id=...,
    client_secret=...,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
```

`server_metadata_url` = discovery automatico.

## SSO — Single Sign-On

| Approccio | Quando |
|-----------|--------|
| OIDC SSO | Moderno, web/mobile/API |
| SAML 2.0 | Enterprise legacy |
| Kerberos | Intranet AD |

> **Mai SSO custom**. Usa Okta/Auth0/Keycloak/Authentik.

## Refresh Token Rotation

- **Access token**: breve (15-30 min) — JWT in `Authorization: Bearer`
- **Refresh token**: lungo (7-30 gg) — opaco, in cookie HttpOnly

Quando access scade → client usa refresh per nuovo, **senza login**.

## Rotation pattern

1. Client usa `refresh_v1` per nuovo access
2. Server emette `access_v2` + `refresh_v2`
3. `refresh_v1` invalidato (status: USED)

Vantaggio: detection riuso.

## Reuse Detection

Se `refresh_v1` viene presentato **due volte**:

→ Furto rilevato.
→ **Revoke intera famiglia**.
→ Forza re-login utente.

## CSRF — cos'è

L'attaccante fa eseguire **al browser della vittima** una richiesta verso un sito su cui è loggata, senza che lo sappia.

## CSRF — esempio classico

```html
<!-- Su evil.com -->
<form action="https://bank.com/transfer" method="POST">
  <input name="to" value="attacker">
  <input name="amount" value="10000">
</form>
<script>document.forms[0].submit();</script>
```

Browser invia POST con cookie sessione bank → bonifico eseguito.

## Difesa A — SameSite cookie

```
Set-Cookie: session=abc; SameSite=Lax; Secure; HttpOnly
```

| Valore | Effetto |
|--------|---------|
| `Strict` | Mai cross-site |
| `Lax` | Solo top-level (default browser) |
| `None` | Sempre (richiede `Secure`) |

## Difesa B — CSRF Token

```html
<form method="POST">
  <input type="hidden" name="csrf_token" value="r4ndom">
  ...
</form>
```

In Flask con Flask-WTF:
```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

## Difesa C — Double-submit cookie (per API)

- Server emette `csrf_cookie` (NON HttpOnly)
- Client legge cookie e lo manda anche come header `X-CSRF-Token`
- Server: cookie == header?

Browser invia cookie automaticamente. JS evil.com non può leggere cookie bank.com → no header → blocco.

## Difesa D — Custom request header

```javascript
fetch("/api", {
  headers: {"X-Requested-With": "XMLHttpRequest"}
})
```

Browser blocca cross-site con header custom (CORS preflight).

> Solo per API JSON, non form HTML.

## Quando CSRF NON si applica

- Endpoint solo GET (sicuri se non hanno side effect)
- Auth via header (Bearer JS) e NON via cookie
- API state-changing chiamate da app non-browser

## Lab — JWT + Flask completo

Cosa includere:

- Login → access + refresh
- Endpoint protetto `@require_jwt`
- Endpoint admin `@require_role("admin")`
- `/refresh` con rotation + reuse detection

> Codice completo nel file `02_lab/M_EXTRA_jwt_lab.py`

## Test attacchi

```bash
# alg: none → pyjwt rifiuta (whitelist)
# Token scaduto → 401 token expired
# Refresh reuse → 401 + revoke famiglia
# Audience mismatch → 401
```

## Checklist JWT/OAuth

- [ ] `algorithms=["HS256"]` whitelist
- [ ] Mai `alg: none`
- [ ] Secret >= 256 bit CSPRNG
- [ ] `exp` < 1h
- [ ] `aud` e `iss` validati
- [ ] Refresh token con rotation
- [ ] Reuse detection
- [ ] JWT in cookie HttpOnly per webapp
- [ ] `state` su OAuth (anti-CSRF)
- [ ] PKCE obbligatorio per app pubbliche
- [ ] `redirect_uri` whitelist

## Checklist CSRF

- [ ] `SameSite=Lax`/`Strict` cookie sessione
- [ ] CSRF token su POST/PUT/DELETE form
- [ ] Token per-request (non globale)
- [ ] Token NON in GET URL
- [ ] Header custom per API JSON
- [ ] State-changing solo POST/PUT/DELETE

## Antipattern

❌ JWT in localStorage
❌ Token vita eterna
❌ Stesso JWT per tutto (no aud)
❌ Refresh senza rotation
❌ OAuth senza `state`
❌ `redirect_uri` aperto
❌ CSRF token globale
❌ Auth solo lato client

## Risorse

- PortSwigger Academy — JWT
- OWASP JWT Cheat Sheet
- OAuth 2.0 Simplified (Aaron Parecki)
- NIST SP 800-63

## Domande?
