# EXTRA — Input Validation & Sanitization

**Materiale integrativo — Corso ITS Cybersecurity**
**Tipologia**: estensione di M6 (web app security)
**Tempo suggerito**: 2-3 ore (lettura + lab)
**Prerequisiti**: M6.2 (SQL Injection), M6.5 (XSS), M6.7 (Path Traversal)

> Capitolo dedicato a un argomento trasversale a quasi tutte le vulnerabilità web. Nel corso base è disseminato in M6, qui è messo insieme con metodo.

---

## Indice

- [1. Validation, Sanitization, Encoding — chi fa cosa](#cap1)
- [2. Whitelist vs Blacklist](#cap2)
- [3. Type validation in Python — Pydantic](#cap3)
- [4. Regex — usi e abusi](#cap4)
- [5. Sanitizzazione HTML — bleach](#cap5)
- [6. Validation per tipo di dato](#cap6)
- [7. Schema validation — JSON Schema](#cap7)
- [8. Lab pratico — form complesso con tutte le difese](#cap8)
- [9. Antipattern frequenti](#cap9)

---

<a name="cap1"></a>
## 1. Validation, Sanitization, Encoding — chi fa cosa

Tre operazioni **diverse**, spesso confuse:

### 1.1 Validation

> **Verifica** che l'input rispetti regole (tipo, formato, range). Se non rispetta, **rifiuta**.

Esempio:
```python
if not isinstance(age, int) or age < 0 or age > 150:
    raise ValueError("età non valida")
```

### 1.2 Sanitization

> **Modifica** l'input per renderlo sicuro. Mantiene il dato ma rimuove parti pericolose.

Esempio:
```python
import bleach
safe_html = bleach.clean(user_html, tags=["p", "b", "i"])
```

### 1.3 Encoding (output)

> **Trasforma** l'output a seconda del contesto (HTML, SQL, shell, JSON). NON modifica il dato in DB.

Esempio:
```html
<!-- Jinja2 fa HTML encoding di default -->
<p>{{ user_name }}</p>
```

### 1.4 Quando usare cosa

| Situazione | Tecnica |
|------------|---------|
| Input strutturato (form, API) | **Validation** (Pydantic, regex) |
| Input ricco (commenti HTML) | **Sanitization** (bleach) + Validation |
| Output in HTML | **Encoding** (Jinja2 auto) |
| Output in SQL | **Parametrizzazione** (NON encoding manuale) |
| Output in shell | **Quoting** (shlex.quote, evitare shell del tutto) |
| Output in JSON | **Standard library** (json.dumps) |

> **Regola d'oro**: validate **all'entrata**, encode **all'uscita**, sanitizza solo se l'input deve mantenere struttura ricca (HTML, markdown).

---

<a name="cap2"></a>
## 2. Whitelist vs Blacklist

### 2.1 Blacklist — "blocca questi caratteri"

```python
# 🚩 ANTI-PATTERN
def sanitize(s):
    forbidden = ["'", ";", "--", "<script>"]
    for f in forbidden:
        s = s.replace(f, "")
    return s
```

Problemi:
- Liste sempre incomplete (encoding, varianti, Unicode lookalike)
- L'attaccante è creativo, tu no.
- Esempi di bypass:
  - `<script>` → `<ScRiPt>`, `<scr<script>ipt>`, `<%73cript>`, ...
  - `'` → `'`, `&#x27;`, `%27`, ...

### 2.2 Whitelist — "accetta solo questi"

```python
# ✅ PATTERN
import re
def is_valid_username(s):
    return bool(re.fullmatch(r"[a-zA-Z0-9_]{3,20}", s))
```

Vantaggi:
- Definito (sai esattamente cosa accetti).
- Rifiuta tutto ciò che non rientra.
- Se serve aggiungere caratteri, li aggiungi consapevolmente.

### 2.3 Regola

> **Whitelist sempre. Blacklist mai.**

Eccezione: filtraggio **assistito** (es. WAF in defense in depth). Ma mai come **unica** difesa.

---

<a name="cap3"></a>
## 3. Type validation in Python — Pydantic

### 3.1 Cos'è Pydantic

Libreria Python per **validation declarativa** basata su type hints. Standard de facto in FastAPI.

```bash
pip install pydantic[email]
```

### 3.2 Esempio base

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date

class Iscrizione(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    age: int = Field(ge=18, le=120)
    birthdate: date
    password: str = Field(min_length=12)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if not any(c.isupper() for c in v): raise ValueError("manca maiuscola")
        if not any(c.islower() for c in v): raise ValueError("manca minuscola")
        if not any(c.isdigit() for c in v): raise ValueError("manca numero")
        return v
```

Uso:
```python
try:
    data = Iscrizione(**request.json)
except ValidationError as e:
    return jsonify({"errors": e.errors()}), 400
```

### 3.3 Cosa Pydantic fa per te

- ✅ Type checking runtime
- ✅ Coercion (es. `"42"` → `42` se int)
- ✅ Validators custom
- ✅ Errori dettagliati con path JSON
- ✅ JSON Schema generation
- ✅ `EmailStr`, `HttpUrl`, `IPvAnyAddress`, `UUID`, `SecretStr`
- ✅ Strict mode (no coercion silenziosa)

### 3.4 Pattern: input model vs DB model

```python
# Input dall'utente (validation rigorosa)
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12)
    name: str = Field(min_length=1, max_length=100)

# Output API (filtro campi)
class UserPublic(BaseModel):
    id: int
    email: EmailStr
    name: str
    # NON: password_hash, role, is_admin, created_at_internal

# Modello DB (separato)
class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    name = Column(String)
    role = Column(String, default="user")
    is_admin = Column(Boolean, default=False)
```

3 modelli separati = 3 layers di sicurezza.

---

<a name="cap4"></a>
## 4. Regex — usi e abusi

### 4.1 Quando regex è OK

- Username (alphanumeric + `_`/`-`)
- Codici (CAP italiano, codice fiscale, IBAN — ma meglio libreria specializzata)
- Slug URL (`[a-z0-9-]+`)
- Pattern semplici a struttura nota

### 4.2 Quando regex è MALE

- **Email**: la regex "vera" RFC 5322 è impossibile. Usa libreria (`email-validator`, Pydantic `EmailStr`).
- **URL**: usa `urllib.parse` + validazione struttura.
- **HTML**: **MAI**. Usa parser (lxml, BeautifulSoup).
- **JSON/XML**: usa parser, non regex.
- **Numeri di carta**: usa libreria (luhn check + bin lookup).

### 4.3 ReDoS — Regular expression Denial of Service

Regex "innocenti" possono essere catastrofiche su input crafted:

```python
# 🚩 VULNERABILE — backtracking esponenziale
import re
re.match(r"^(a+)+$", "a" * 30 + "!")
# ~5 secondi su input di 30 caratteri
```

Difesa:
- Evitare regex con quantificatori annidati (`(a+)+`, `(a*)*`)
- Usare libreria con timeout (`re2`, `regex` con timeout)
- Validare lunghezza input PRIMA di regex
- Tool di analisi: https://devina.io/redos-checker

### 4.4 Esempi corretti

```python
import re

# Username: 3-20 caratteri alfanumerici + underscore
USERNAME = re.compile(r"^[a-zA-Z0-9_]{3,20}$")

# CAP italiano
CAP = re.compile(r"^\d{5}$")

# Slug URL
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Email — NON usare, usa email-validator
# EMAIL = re.compile(r"...")  # non farlo
```

---

<a name="cap5"></a>
## 5. Sanitizzazione HTML — bleach

### 5.1 Quando serve

L'utente deve poter scrivere HTML "ricco" (commenti con grassetto, link, ecc.) ma **non** script o iframe malevoli.

Casi tipici: piattaforme blogging, commenti, forum, CMS.

### 5.2 bleach — la libreria

```bash
pip install bleach
```

```python
import bleach

ALLOWED_TAGS = ["p", "b", "strong", "i", "em", "u", "a", "ul", "ol", "li", "br", "code", "pre"]
ALLOWED_ATTRS = {"a": ["href", "title"], "*": ["class"]}
ALLOWED_PROTO = ["http", "https", "mailto"]

clean = bleach.clean(
    user_html,
    tags=ALLOWED_TAGS,
    attributes=ALLOWED_ATTRS,
    protocols=ALLOWED_PROTO,
    strip=True,        # rimuovi tag non ammessi (vs escape)
)
```

### 5.3 Esempi di trasformazione

| Input | Output `bleach` |
|-------|----------------|
| `<p>Ciao</p>` | `<p>Ciao</p>` ✅ |
| `<p>Ciao <script>alert(1)</script></p>` | `<p>Ciao </p>` (script rimosso) |
| `<a href="javascript:alert(1)">x</a>` | `<a>x</a>` (href rimosso, javascript: non in protocolli) |
| `<a href="https://example.com">x</a>` | `<a href="https://example.com">x</a>` ✅ |

### 5.4 Alternative

- **markdown** + sanitization: invece di accettare HTML, accetti Markdown e lo converti server-side. Più sicuro perché il superset di output è limitato.
- **DOMPurify** (lato client JS): per sanitizzare HTML prima di inserirlo nel DOM. Per webapp con WYSIWYG.

### 5.5 Pattern — escape vs sanitize

| Caso | Cosa fare |
|------|-----------|
| Input semplice (username, titolo) | **Validate** + escape output (Jinja2 default) |
| Input HTML "ricco" voluto | **Sanitize** con bleach |
| Output in attributo HTML | Encoding diverso (es. `data-*` con JSON.stringify) |
| Output in JS string | `json.dumps` (genera string JSON sicura) |
| Output in URL | `urllib.parse.quote` |

---

<a name="cap6"></a>
## 6. Validation per tipo di dato

### 6.1 Email

```python
from email_validator import validate_email, EmailNotValidError
try:
    info = validate_email(input_email, check_deliverability=False)
    normalized = info.normalized
except EmailNotValidError:
    raise ValueError("email non valida")
```

In Pydantic: `EmailStr`.

### 6.2 URL

```python
from urllib.parse import urlparse
def is_safe_url(url: str) -> bool:
    try:
        p = urlparse(url)
    except ValueError:
        return False
    return p.scheme in {"http", "https"} and bool(p.netloc)
```

Per validazione completa: Pydantic `HttpUrl`.

### 6.3 Filename / Path

```python
import re
SAFE_FILENAME = re.compile(r"^[a-zA-Z0-9._-]{1,100}$")

def safe_filename(s: str) -> str:
    if not SAFE_FILENAME.fullmatch(s):
        raise ValueError("filename non valido")
    if s.startswith(".") or "/" in s or "\\" in s:
        raise ValueError("filename non valido")
    return s
```

### 6.4 Numeri (range, precisione)

```python
from decimal import Decimal
def parse_money(s: str) -> Decimal:
    try:
        d = Decimal(s)
    except InvalidOperation:
        raise ValueError("importo non valido")
    if d <= 0 or d > Decimal("1000000"):
        raise ValueError("importo fuori range")
    if d.as_tuple().exponent < -2:
        raise ValueError("max 2 decimali")
    return d
```

### 6.5 Date e timestamp

```python
from datetime import date
class Iscrizione(BaseModel):
    birthdate: date

    @field_validator("birthdate")
    def not_future(cls, v):
        if v > date.today():
            raise ValueError("data nel futuro")
        if (date.today() - v).days < 18*365:
            raise ValueError("minorenne")
        return v
```

### 6.6 IBAN, codice fiscale

Usa librerie specializzate:

```python
from schwifty import IBAN
try:
    iban = IBAN(input_iban)
except ValueError:
    raise ValueError("IBAN non valido")
```

```python
from codicefiscale import codicefiscale
if not codicefiscale.is_valid(input_cf):
    raise ValueError("codice fiscale non valido")
```

### 6.7 File upload

Validare:
- **Estensione** (whitelist)
- **MIME type** (libmagic, non solo header HTTP)
- **Dimensione** (max)
- **Contenuto effettivo** (es. è davvero un PNG? `Pillow` per immagini)

```python
import magic
from PIL import Image

def validate_image(content: bytes, max_size: int = 5*1024*1024) -> None:
    if len(content) > max_size:
        raise ValueError("file troppo grande")

    mime = magic.from_buffer(content, mime=True)
    if mime not in {"image/png", "image/jpeg"}:
        raise ValueError(f"MIME non ammesso: {mime}")

    try:
        img = Image.open(io.BytesIO(content))
        img.verify()
    except Exception:
        raise ValueError("immagine corrotta o sospetta")
```

---

<a name="cap7"></a>
## 7. Schema validation — JSON Schema

Per API che accettano JSON complessi, validation dichiarativa basata su standard.

### 7.1 Definire schema

```python
schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 3, "maxLength": 20,
                     "pattern": "^[a-zA-Z0-9_]+$"},
        "age": {"type": "integer", "minimum": 18, "maximum": 120},
        "email": {"type": "string", "format": "email"},
        "tags": {"type": "array", "items": {"type": "string"}, "maxItems": 5},
    },
    "required": ["username", "email"],
    "additionalProperties": False,        # ⚠️ rifiuta campi extra
}
```

### 7.2 Validare

```python
from jsonschema import validate, ValidationError
try:
    validate(instance=request.json, schema=schema)
except ValidationError as e:
    return jsonify({"error": str(e)}), 400
```

### 7.3 Pydantic vs JSON Schema

| | Pydantic | JSON Schema |
|---|----------|-------------|
| DSL | Python | JSON |
| Coercion | Sì (default) | No |
| IDE support | Eccellente | Limitato |
| Cross-language | No | Sì (JS, Java, Go...) |
| Quando usare | App Python | API multi-language, contract-first |

**FastAPI usa entrambi**: definisci con Pydantic, FastAPI genera JSON Schema per OpenAPI.

---

<a name="cap8"></a>
## 8. Lab pratico — form complesso con tutte le difese

### 8.1 Scenario

Form di registrazione utente per una piattaforma "social per professionisti":
- Username (alfanumerico, 3-20)
- Email
- Password robusta
- Data di nascita (>= 18 anni)
- Bio in HTML "ricco" (b, i, a, p, br)
- URL profilo opzionale (HTTP/HTTPS)
- Foto profilo (PNG/JPG, max 5MB)
- Lista skill (max 10 stringhe alfanumeriche)

### 8.2 Modello Pydantic

```python
from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator
from datetime import date
import bleach

ALLOWED_TAGS = ["p", "b", "strong", "i", "em", "a", "br"]
ALLOWED_ATTRS = {"a": ["href", "title"]}
ALLOWED_PROTO = ["http", "https"]


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    birthdate: date
    bio: str | None = Field(default=None, max_length=2000)
    profile_url: HttpUrl | None = None
    skills: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("password")
    @classmethod
    def strong_password(cls, v):
        rules = [
            (any(c.isupper() for c in v), "manca maiuscola"),
            (any(c.islower() for c in v), "manca minuscola"),
            (any(c.isdigit() for c in v), "manca numero"),
            (any(not c.isalnum() for c in v), "manca speciale"),
        ]
        for ok, msg in rules:
            if not ok:
                raise ValueError(msg)
        return v

    @field_validator("birthdate")
    @classmethod
    def adult(cls, v):
        from datetime import date
        if (date.today() - v).days < 18 * 365:
            raise ValueError("devi essere maggiorenne")
        return v

    @field_validator("bio")
    @classmethod
    def sanitize_bio(cls, v):
        if v is None:
            return None
        return bleach.clean(v, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS,
                            protocols=ALLOWED_PROTO, strip=True)

    @field_validator("skills")
    @classmethod
    def valid_skills(cls, v):
        for s in v:
            if not s.replace("-", "").replace(" ", "").isalnum():
                raise ValueError(f"skill non valida: {s}")
            if len(s) > 50:
                raise ValueError("skill troppo lunga")
        return v
```

### 8.3 Endpoint Flask

```python
from flask import Flask, request, jsonify
from pydantic import ValidationError

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register():
    try:
        user = UserCreate(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    # Foto profilo (multipart in produzione, qui mock)
    # ... validazione separata foto ...

    # Salvataggio (con bcrypt sulla password!)
    save_user(user)

    return jsonify({"status": "created", "username": user.username}), 201
```

### 8.4 Test casi limite

```python
import pytest

def test_username_invalido():
    with pytest.raises(ValidationError):
        UserCreate(username="ab", email="x@y.com", password="Abcdef1!xyz12",
                   birthdate=date(2000, 1, 1))

def test_email_malformata():
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="non-email",
                   password="Abcdef1!xyz12", birthdate=date(2000,1,1))

def test_password_debole():
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="x@y.com",
                   password="password", birthdate=date(2000,1,1))

def test_minorenne():
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="x@y.com",
                   password="Abcdef1!xyz12",
                   birthdate=date(2020, 1, 1))

def test_xss_in_bio():
    u = UserCreate(username="alice", email="x@y.com",
                   password="Abcdef1!xyz12", birthdate=date(2000,1,1),
                   bio='<script>alert(1)</script><p>Ciao</p>')
    assert "<script>" not in u.bio
    assert "<p>" in u.bio

def test_url_javascript():
    u = UserCreate(username="alice", email="x@y.com",
                   password="Abcdef1!xyz12", birthdate=date(2000,1,1),
                   bio='<a href="javascript:alert(1)">x</a>')
    assert "javascript" not in u.bio.lower()

def test_skill_overflow():
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="x@y.com",
                   password="Abcdef1!xyz12", birthdate=date(2000,1,1),
                   skills=["s"] * 11)
```

> Esegui con `pytest`. Vedi che ogni edge case è coperto.

---

<a name="cap9"></a>
## 9. Antipattern frequenti

| Antipattern | Conseguenza |
|-------------|-------------|
| Solo client-side validation | Bypass banale (curl) |
| Blacklist di caratteri | Sempre incompleta |
| Regex su email/URL "creata a mano" | Falsi negativi/positivi |
| `eval()` o `exec()` su input utente | RCE |
| `pickle.loads()` su dati untrusted | RCE |
| HTML escaping con `replace("<", "&lt;")` | Caso edge: incomplete |
| Validazione "after sanitization" senza re-check | Bypass |
| Non limitare lunghezza input prima di regex | ReDoS |
| Non validare extension MIME del file | Upload .exe come .jpg |
| Trusting `Content-Type` header | Spoofable, usa libmagic |

---

## Per approfondire

- **OWASP Input Validation Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- **Pydantic Documentation**: https://docs.pydantic.dev
- **bleach Documentation**: https://bleach.readthedocs.io
- **OWASP Mass Assignment Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html

---

> **Suggerimento di integrazione**:
> - Inserire **prima** di M6.2 (SQL Injection) come "M6.0 — Input Validation as Foundation"
> - Sostituire le 30 sec di "Validation aggiuntiva" sparse in M6 con questo capitolo unico (1h)
> - Lab opzionale di 1.5h sul form complesso
