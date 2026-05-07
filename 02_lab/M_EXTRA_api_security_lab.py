"""
Lab EXTRA — FastAPI con difese OWASP API Top 10

Obiettivi del lab:
1. Costruire API REST con FastAPI + Pydantic
2. Difendere da BOLA (API1)
3. Difendere da BOPLA (API3) con Pydantic input/output models
4. Implementare rate limiting (API4)
5. Implementare function-level authz (API5)
6. Testare gli attacchi e verificare le difese

INSTALLAZIONE:
    pip install fastapi uvicorn "pydantic[email]" python-jose[cryptography] slowapi

USO:
    uvicorn M_EXTRA_api_security_lab:app --reload
    # Apri http://localhost:8000/docs per Swagger UI

LIVELLO: avanzato
"""

import time
import secrets
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field
from jose import jwt, JWTError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


# === CONFIGURAZIONE ===
SECRET = secrets.token_urlsafe(64)
ALGO = "HS256"
TTL = 15 * 60

app = FastAPI(title="API Security Demo", version="1.0")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# === MOCK DB ===
USERS = {
    "alice": {"id": 1, "password": "alice123", "role": "user"},
    "bob": {"id": 2, "password": "bob123", "role": "user"},
    "admin": {"id": 3, "password": "admin123", "role": "admin"},
}

ORDERS = [
    {"id": 100, "user_id": 1, "amount": 50.0,
     "secret_internal_score": 75},
    {"id": 101, "user_id": 1, "amount": 200.0,
     "secret_internal_score": 80},
    {"id": 102, "user_id": 2, "amount": 30.0,
     "secret_internal_score": 60},
    {"id": 103, "user_id": 3, "amount": 1000.0,
     "secret_internal_score": 99},
]


# === PYDANTIC MODELS ===
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserPublic(BaseModel):
    """Response model — NON include password, secret_internal."""
    id: int
    username: str
    role: str


class OrderPublic(BaseModel):
    """Response model — NON include secret_internal_score."""
    id: int
    user_id: int
    amount: float


class OrderUpdate(BaseModel):
    """Request model — solo `amount` modificabile.

    Senza questo, attaccante potrebbe inviare:
        {"amount": 100, "user_id": 999, "secret_score": 1000}
    e mass-assignment lo accetterebbe.
    """
    amount: float = Field(gt=0, le=1_000_000)


# === AUTH ===
def make_token(username: str, role: str) -> str:
    return jwt.encode({
        "sub": username,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + TTL,
        "iss": "myapi",
        "aud": "myclients",
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
    """API5: function-level authz."""
    if user["role"] != "admin":
        raise HTTPException(403, "admin only")
    return user


# === ENDPOINTS ===
@app.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")        # API4: rate limit
async def login(request: Request, username: str, password: str):
    u = USERS.get(username)
    if not u or u["password"] != password:
        # In produzione: bcrypt + risposta uniforme
        raise HTTPException(401, "invalid credentials")
    return TokenResponse(access_token=make_token(username, u["role"]))


@app.get("/me", response_model=UserPublic)
def me(user=Depends(current_user)):
    return UserPublic(id=user["id"], username=user["username"], role=user["role"])


@app.get("/orders", response_model=list[OrderPublic])
def my_orders(user=Depends(current_user)):
    """API1: BOLA prevenuto.

    NON usa user_id da URL. Usa quello dal token.
    """
    return [OrderPublic(**o) for o in ORDERS if o["user_id"] == user["id"]]


@app.get("/orders/{oid}", response_model=OrderPublic)
def get_order(oid: int, user=Depends(current_user)):
    """API1: ownership check esplicito."""
    o = next((o for o in ORDERS if o["id"] == oid), None)
    if not o:
        raise HTTPException(404)
    if o["user_id"] != user["id"] and user["role"] != "admin":
        raise HTTPException(403, "forbidden")
    return OrderPublic(**o)


@app.put("/orders/{oid}", response_model=OrderPublic)
def update_order(oid: int, payload: OrderUpdate, user=Depends(current_user)):
    """API3: BOPLA prevenuto.

    OrderUpdate accetta SOLO `amount`. Campi extra ignorati.
    """
    o = next((o for o in ORDERS if o["id"] == oid), None)
    if not o or o["user_id"] != user["id"]:
        raise HTTPException(403)
    o["amount"] = payload.amount
    return OrderPublic(**o)


@app.get("/admin/orders", response_model=list[OrderPublic])
def all_orders(_=Depends(require_admin)):
    """API5: solo admin può vedere tutti gli ordini."""
    return [OrderPublic(**o) for o in ORDERS]


# =====================================================================
# TEST RED TEAM
# =====================================================================
#
# Avvio: uvicorn M_EXTRA_api_security_lab:app --reload
# Swagger: http://localhost:8000/docs
#
# 1) LOGIN come alice
#    curl -X POST 'http://localhost:8000/login?username=alice&password=alice123'
#    → {"access_token":"...","token_type":"bearer"}
#    Salva il token in $T
#
# 2) ENDPOINT NORMALE
#    curl http://localhost:8000/me -H "Authorization: Bearer $T"
#    → vede solo i suoi dati
#
# 3) BOLA TEST (API1)
#    curl http://localhost:8000/orders -H "Authorization: Bearer $T"
#    → vede SOLO i suoi ordini (id 100, 101)
#
#    curl http://localhost:8000/orders/102 -H "Authorization: Bearer $T"
#    → 403 (è di bob)
#
#    curl http://localhost:8000/orders/103 -H "Authorization: Bearer $T"
#    → 403 (è di admin)
#
# 4) BOPLA TEST (API3)
#    curl -X PUT http://localhost:8000/orders/100 \
#      -H "Authorization: Bearer $T" \
#      -H "Content-Type: application/json" \
#      -d '{"amount": 75, "user_id": 999, "secret_score": 1000}'
#    → 200 OK, amount=75
#    → I campi extra (user_id, secret_score) sono IGNORATI
#    → Pydantic OrderUpdate accetta solo `amount`
#
# 5) RESPONSE MODEL (excessive data exposure prevenuto)
#    Le risposte NON includono `secret_internal_score`,
#    anche se è nel mock DB.
#    → Pydantic OrderPublic filtra per design
#
# 6) FUNCTION-LEVEL AUTHZ (API5)
#    curl http://localhost:8000/admin/orders -H "Authorization: Bearer $T"
#    → 403 (alice non è admin)
#
#    Login come admin, ripeti:
#    → 200 con tutti gli ordini
#
# 7) RATE LIMIT (API4)
#    Esegui 6 volte rapidamente:
#    for i in {1..6}; do
#      curl -X POST 'http://localhost:8000/login?username=alice&password=wrong'
#    done
#    → Le prime 5: 401
#    → La 6ª: 429 Too Many Requests
#
# =====================================================================
# ESERCIZI DI APPROFONDIMENTO
# =====================================================================
#
# E1) Aggiungi un endpoint /api/users/{uid} pubblico (no auth).
#     Ti rendi conto che è BOLA gigante: chiunque vede dati di tutti.
#     Aggiungi auth + ownership check.
#
# E2) Estendi OrderUpdate per supportare anche `description: str`.
#     Verifica che `user_id` resti immutabile.
#
# E3) Aggiungi pagination obbligatoria a /orders:
#       def my_orders(limit: int = 20, offset: int = 0):
#         limit = min(limit, 100)
#     Cosa succede se l'attaccante mette ?limit=999999?
#
# E4) Aggiungi un endpoint /api/proxy?url=... che fetcha l'URL.
#     IMPLEMENTA SSRF DEFENSE:
#     - whitelist domini
#     - blocca IP privati (169.254.x, 10.x, 192.168.x, 127.x)
#     - blocca protocolli non-HTTP
#
# E5) Aggiungi webhook endpoint /webhook con verifica HMAC.
#     Senza secret, chiunque può chiamarlo.
#     Implementa firma con header X-Signature.
#
# =====================================================================
# DOMANDE
# =====================================================================
#
# Q1: Cosa significa BOLA? Differenza con IDOR?
# Q2: Perché Pydantic protegge da Mass Assignment?
# Q3: Cosa fa response_model in FastAPI?
# Q4: Come SSRF su Capital One ha rubato 100M record?
# Q5: Quando bisogna usare 401 invece di 403?
# Q6: Cos'è il "discovery endpoint" OIDC?
# Q7: Quale è il vector di attacco di OAuth se manca PKCE?
