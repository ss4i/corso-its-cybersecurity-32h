---
title: "EXTRA — Input Validation & Sanitization"
subtitle: "Corso ITS Cybersecurity — Modulo Avanzato"
author: "Ing. Alessandro Manneschi"
date: "ITS Prodigi · ITS Empoli · SS4I"
---

# EXTRA — Input Validation
## 2-3 ore — Pydantic, regex, sanitization

## Obiettivi

- Validation, sanitization, encoding — chi fa cosa
- Whitelist vs Blacklist
- **Pydantic** approfondito
- Regex sicuro (e ReDoS)
- **bleach** per HTML
- Validation per tipo (email, URL, file)
- Lab form complesso

## I 3 concetti — non confonderli

| | Cosa fa | Esempio |
|---|---------|---------|
| **Validation** | Verifica + rifiuta | `if not isinstance(age, int): raise` |
| **Sanitization** | Modifica + tiene | `bleach.clean(html)` |
| **Encoding** | Trasforma in output | Jinja2 `{{ x }}` |

## Quando usare cosa

| Situazione | Tecnica |
|------------|---------|
| Input strutturato | **Validation** (Pydantic, regex) |
| Input HTML ricco | **Sanitization** (bleach) |
| Output HTML | **Encoding** (Jinja2 auto) |
| Output SQL | **Parametrizzazione** |
| Output shell | **Quoting** (o evita shell) |

## Regola d'oro

> **Validate** all'entrata
> **Encode** all'uscita
> **Sanitize** solo se serve struttura ricca

## Whitelist vs Blacklist

```python
# 🚩 BLACKLIST (sbagliato)
forbidden = ["'", ";", "<script>"]
for f in forbidden:
    s = s.replace(f, "")
```

Bypass infiniti: `<ScRiPt>`, `&#x27;`, ecc.

## Whitelist (giusto)

```python
# ✅ WHITELIST
import re
def is_valid_username(s):
    return bool(re.fullmatch(r"[a-zA-Z0-9_]{3,20}", s))
```

Definito, controllato, esplicito.

## La regola

> **Whitelist sempre. Blacklist mai.**

Eccezione: WAF in defense in depth, mai come unica difesa.

## Pydantic — cos'è

Validation **declarativa** Python basata su type hints.

```bash
pip install pydantic[email]
```

Standard de facto in FastAPI.

## Pydantic — esempio

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import date

class Iscrizione(BaseModel):
    username: str = Field(min_length=3, max_length=20,
                          pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    age: int = Field(ge=18, le=120)
    birthdate: date
    password: str = Field(min_length=12)
```

## Validators custom

```python
class Iscrizione(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def strong(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("manca maiuscola")
        if not any(c.isdigit() for c in v):
            raise ValueError("manca numero")
        return v
```

## Pattern — 3 modelli separati

```python
# Input dall'utente
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

# Output API
class UserPublic(BaseModel):
    id: int
    email: EmailStr
    name: str
    # NO: password_hash

# DB model (separato)
class User(Base):
    id, email, password_hash, role, ...
```

## Regex — quando OK

- Username, slug, codici (CAP)
- Pattern semplici a struttura nota

## Regex — quando MALE

| Cosa | Perché |
|------|--------|
| Email | RFC 5322 impossibile |
| URL | Usa urllib.parse |
| HTML | Usa parser (lxml) |
| JSON/XML | Usa parser |
| Numeri carta | Usa libreria luhn |

## ReDoS — Regular expression DoS

```python
# 🚩 BACKTRACKING ESPONENZIALE
re.match(r"^(a+)+$", "a"*30 + "!")
# ~5 secondi su 30 chars
```

Difesa:
- No quantificatori annidati
- Validate length **prima** di regex
- Tool: devina.io/redos-checker

## Sanitizzazione HTML — bleach

Quando l'utente deve scrivere HTML "ricco" (commenti, profilo).

```python
import bleach

clean = bleach.clean(
    user_html,
    tags=["p", "b", "i", "a"],
    attributes={"a": ["href"]},
    protocols=["http", "https"],
    strip=True,
)
```

## bleach — esempi

| Input | Output |
|-------|--------|
| `<p>Ciao</p>` | `<p>Ciao</p>` ✅ |
| `<script>alert(1)</script>` | rimosso |
| `<a href="javascript:...">x</a>` | `<a>x</a>` |
| `<a href="https://...">x</a>` | OK ✅ |

## Validation per tipo — Email

```python
from email_validator import validate_email
try:
    info = validate_email(input_email)
    normalized = info.normalized
except EmailNotValidError:
    raise ValueError("email")
```

In Pydantic: `EmailStr`.

## Validation per tipo — URL

```python
from urllib.parse import urlparse
def is_safe_url(url):
    p = urlparse(url)
    return p.scheme in {"http", "https"} and bool(p.netloc)
```

In Pydantic: `HttpUrl`.

## Validation per tipo — Filename

```python
SAFE_FILENAME = re.compile(r"^[a-zA-Z0-9._-]{1,100}$")

def safe_filename(s):
    if not SAFE_FILENAME.fullmatch(s):
        raise ValueError
    if s.startswith(".") or "/" in s:
        raise ValueError
    return s
```

## Validation per tipo — Money

```python
from decimal import Decimal
def parse_money(s):
    d = Decimal(s)
    if d <= 0 or d > 1_000_000:
        raise ValueError("range")
    if d.as_tuple().exponent < -2:
        raise ValueError("max 2 decimali")
    return d
```

## Validation file upload

Validare:
- **Estensione** (whitelist)
- **MIME** (libmagic, NO header HTTP)
- **Dimensione**
- **Contenuto** (es. Pillow per immagine)

## File validation — esempio

```python
import magic
from PIL import Image

def validate_image(content, max_size=5*1024*1024):
    if len(content) > max_size:
        raise ValueError("size")
    mime = magic.from_buffer(content, mime=True)
    if mime not in {"image/png", "image/jpeg"}:
        raise ValueError("mime")
    Image.open(io.BytesIO(content)).verify()
```

## JSON Schema

```python
schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 3},
        "age": {"type": "integer", "minimum": 18},
    },
    "required": ["username"],
    "additionalProperties": False,  # ⚠️ rifiuta extra
}

from jsonschema import validate
validate(request.json, schema)
```

## Pydantic vs JSON Schema

| | Pydantic | JSON Schema |
|---|----------|-------------|
| DSL | Python | JSON |
| Coercion | Sì | No |
| IDE | ✅ | Limitato |
| Cross-language | No | Sì |

FastAPI: usa Pydantic + genera JSON Schema.

## Lab — form complesso

Form di registrazione con:
- Username alfanum
- EmailStr
- Password robusta (4 regole)
- Data nascita >= 18 anni
- Bio in HTML "ricco" (b, i, a)
- URL profilo HTTPS
- Foto PNG/JPG max 5MB
- Skills list (max 10)

> Codice in `02_lab/M_EXTRA_input_validation_lab.py`

## Test casi limite

```python
def test_username_invalido():
    with pytest.raises(ValidationError):
        UserCreate(username="ab", ...)

def test_xss_in_bio():
    u = UserCreate(bio='<script>alert(1)</script><p>OK</p>', ...)
    assert "<script>" not in u.bio
    assert "<p>" in u.bio

def test_minorenne():
    with pytest.raises(ValidationError):
        UserCreate(birthdate=date(2020,1,1), ...)
```

## Antipattern

| Anti | Conseguenza |
|------|-------------|
| Solo client-side | Bypass curl |
| Blacklist caratteri | Sempre incomplete |
| Regex email manuale | Falsi positivi/negativi |
| `eval()` su input | RCE |
| `pickle.loads()` untrusted | RCE |
| No length limit prima di regex | ReDoS |
| Trust `Content-Type` | MIME spoofing |

## Risorse

- OWASP Input Validation Cheat Sheet
- Pydantic docs
- bleach docs
- OWASP Mass Assignment Cheat Sheet

## Domande?
