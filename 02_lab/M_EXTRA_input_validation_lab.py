"""
Lab EXTRA — Input Validation con Pydantic + bleach

Obiettivi del lab:
1. Form complesso con tutte le difese
2. Pydantic con field_validator custom
3. Sanitization HTML con bleach
4. Validation per tipo (email, URL, password, file)
5. Test casi limite (XSS, SQLi pattern, minorenne, ecc.)

INSTALLAZIONE:
    pip install pydantic[email] bleach pillow python-magic-bin pytest

NOTA WINDOWS: python-magic richiede file/libmagic.
Su Windows: pip install python-magic-bin
Su macOS: brew install libmagic
Su Linux: sudo apt install libmagic1

USO:
    python M_EXTRA_input_validation_lab.py        # esempi
    pytest M_EXTRA_input_validation_lab.py -v     # test

LIVELLO: intermedio
"""

import io
import re
from datetime import date
from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator, ValidationError
import bleach


# === CONFIGURAZIONE ===
ALLOWED_TAGS = ["p", "b", "strong", "i", "em", "u", "a", "br", "code", "ul", "ol", "li"]
ALLOWED_ATTRS = {"a": ["href", "title"], "*": ["class"]}
ALLOWED_PROTO = ["http", "https", "mailto"]


# === MODELLO PRINCIPALE: Form di registrazione ===
class UserCreate(BaseModel):
    """Modello per registrazione utente con validation rigorosa."""

    username: str = Field(
        min_length=3, max_length=20,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Solo alfanumerici e underscore, 3-20 char",
    )
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    birthdate: date
    bio: str | None = Field(default=None, max_length=2000)
    profile_url: HttpUrl | None = None
    skills: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        """Password robusta: maiuscola, minuscola, numero, speciale."""
        rules = [
            (any(c.isupper() for c in v), "manca lettera maiuscola"),
            (any(c.islower() for c in v), "manca lettera minuscola"),
            (any(c.isdigit() for c in v), "manca numero"),
            (any(not c.isalnum() for c in v), "manca carattere speciale"),
        ]
        for ok, msg in rules:
            if not ok:
                raise ValueError(msg)
        return v

    @field_validator("birthdate")
    @classmethod
    def must_be_adult(cls, v):
        """Almeno 18 anni."""
        if v > date.today():
            raise ValueError("data di nascita nel futuro")
        days_old = (date.today() - v).days
        if days_old < 18 * 365:
            raise ValueError("devi essere maggiorenne")
        return v

    @field_validator("bio")
    @classmethod
    def sanitize_bio(cls, v):
        """Sanitizza HTML con bleach (whitelist tag)."""
        if v is None:
            return None
        return bleach.clean(
            v,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRS,
            protocols=ALLOWED_PROTO,
            strip=True,
        )

    @field_validator("skills")
    @classmethod
    def valid_skills(cls, v):
        """Skills: alfanumerici + spazi/dash, max 50 char ciascuno."""
        for s in v:
            if not re.fullmatch(r"[a-zA-Z0-9 \-]{1,50}", s):
                raise ValueError(f"skill non valida: '{s}'")
        return v


# === FILE UPLOAD VALIDATION ===
def validate_image_upload(content: bytes, max_size: int = 5 * 1024 * 1024) -> dict:
    """Valida un upload immagine.

    Returns: dict con info, raise ValueError se invalido.
    """
    if len(content) > max_size:
        raise ValueError(f"file troppo grande (max {max_size} byte)")

    # Verifica MIME type REALE (non header HTTP, che è spoofabile)
    try:
        import magic
        mime = magic.from_buffer(content, mime=True)
    except ImportError:
        # Fallback senza libmagic: solo verifica magic bytes basico
        if content[:8] == b"\x89PNG\r\n\x1a\n":
            mime = "image/png"
        elif content[:3] == b"\xff\xd8\xff":
            mime = "image/jpeg"
        else:
            mime = "unknown"

    if mime not in {"image/png", "image/jpeg"}:
        raise ValueError(f"tipo file non ammesso: {mime}")

    # Verifica che sia davvero un'immagine (apribile)
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(content))
        img.verify()
        return {"mime": mime, "size": len(content),
                "format": img.format, "dimensions": img.size}
    except Exception as e:
        raise ValueError(f"immagine corrotta: {e}")


# === DEMO ===
def demo():
    """Esempi di uso."""
    print("=" * 60)
    print("DEMO 1: utente valido")
    print("=" * 60)

    user = UserCreate(
        username="alice_2024",
        email="alice@example.com",
        password="Sicura123!Mol",
        birthdate=date(1995, 5, 15),
        bio="<p>Sono <b>Alice</b>, sviluppatrice Python.</p>",
        profile_url="https://example.com/alice",
        skills=["Python", "FastAPI", "Docker"],
    )
    print(f"✓ Utente creato: {user.username}")
    print(f"  Bio sanitizzata: {user.bio}")

    print("\n" + "=" * 60)
    print("DEMO 2: tentativi di XSS bloccati")
    print("=" * 60)

    user_xss = UserCreate(
        username="bob_test",
        email="bob@example.com",
        password="Sicura123!Mol",
        birthdate=date(1990, 1, 1),
        bio='<script>alert("XSS")</script><p>Ciao</p><img src=x onerror=alert(1)>',
    )
    print(f"  Bio originale: contiene <script>, <img onerror>")
    print(f"  Bio dopo bleach: {user_xss.bio}")
    print(f"  → script e img RIMOSSI ✓")

    print("\n" + "=" * 60)
    print("DEMO 3: URL javascript: bloccato in bio")
    print("=" * 60)

    user_js = UserCreate(
        username="charlie",
        email="charlie@example.com",
        password="Sicura123!Mol",
        birthdate=date(1990, 1, 1),
        bio='<a href="javascript:alert(1)">click me</a>',
    )
    print(f"  Bio dopo bleach: {user_js.bio}")
    print(f"  → href javascript: RIMOSSO ✓")

    print("\n" + "=" * 60)
    print("DEMO 4: ERRORI di validation catturati")
    print("=" * 60)

    test_cases = [
        ("username troppo corto",
         {"username": "a"}),
        ("email malformata",
         {"username": "ok123", "email": "non-email"}),
        ("password debole",
         {"username": "ok123", "email": "x@y.com", "password": "password"}),
        ("minorenne",
         {"username": "ok123", "email": "x@y.com",
          "password": "Sicura123!Mol", "birthdate": date(2020, 1, 1)}),
        ("URL non HTTPS",
         {"username": "ok123", "email": "x@y.com",
          "password": "Sicura123!Mol", "birthdate": date(1990, 1, 1),
          "profile_url": "javascript:alert(1)"}),
    ]
    for name, fields in test_cases:
        try:
            UserCreate(**fields)
            print(f"  ✗ {name}: avrebbe dovuto fallire ma è passato!")
        except ValidationError as e:
            print(f"  ✓ {name}: bloccato — {e.errors()[0]['msg'][:50]}")


# === TEST AUTOMATICI (pytest) ===
def test_username_invalido():
    import pytest
    with pytest.raises(ValidationError):
        UserCreate(username="ab", email="x@y.com",
                   password="Sicura123!Mol", birthdate=date(1990, 1, 1))


def test_email_malformata():
    import pytest
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="not-email",
                   password="Sicura123!Mol", birthdate=date(1990, 1, 1))


def test_password_debole():
    import pytest
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="x@y.com",
                   password="password", birthdate=date(1990, 1, 1))


def test_password_no_speciale():
    import pytest
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="x@y.com",
                   password="Sicura12345", birthdate=date(1990, 1, 1))


def test_minorenne():
    import pytest
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="x@y.com",
                   password="Sicura123!Mol", birthdate=date(2020, 1, 1))


def test_xss_in_bio_rimosso():
    u = UserCreate(username="alice", email="x@y.com",
                   password="Sicura123!Mol", birthdate=date(1990, 1, 1),
                   bio='<script>alert(1)</script><p>Ciao</p>')
    assert "<script>" not in u.bio
    assert "<p>" in u.bio
    assert "Ciao" in u.bio


def test_xss_url_javascript_rimosso():
    u = UserCreate(username="alice", email="x@y.com",
                   password="Sicura123!Mol", birthdate=date(1990, 1, 1),
                   bio='<a href="javascript:alert(1)">x</a>')
    assert "javascript" not in u.bio.lower()


def test_skills_overflow():
    import pytest
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="x@y.com",
                   password="Sicura123!Mol", birthdate=date(1990, 1, 1),
                   skills=["s"] * 11)


def test_skill_caratteri_invalidi():
    import pytest
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="x@y.com",
                   password="Sicura123!Mol", birthdate=date(1990, 1, 1),
                   skills=["Python<script>"])


def test_username_caratteri_invalidi():
    import pytest
    with pytest.raises(ValidationError):
        UserCreate(username="alice@bob", email="x@y.com",
                   password="Sicura123!Mol", birthdate=date(1990, 1, 1))


if __name__ == "__main__":
    demo()
    print("\n\nPer eseguire i test: pytest M_EXTRA_input_validation_lab.py -v")


# =====================================================================
# ESERCIZI DI APPROFONDIMENTO
# =====================================================================
#
# E1) Aggiungi un campo `phone: str` con validazione regex per numeri
#     italiani (+39, prefissi mobili 3xx, ecc.).
#
# E2) Aggiungi un campo `iban: str` con validazione tramite libreria
#     `schwifty`:
#         from schwifty import IBAN
#         IBAN(iban_input)  # raise ValueError se invalido
#
# E3) Aggiungi un campo `cf: str` (codice fiscale italiano) con libreria
#     `python-codicefiscale`.
#
# E4) Implementa file upload validation per PDF (max 10MB):
#     - magic.from_buffer → application/pdf
#     - Verifica che sia un PDF apribile (PyPDF2)
#
# E5) Crea un secondo modello `UserUpdate` (per PATCH) dove TUTTI i campi
#     sono opzionali ma con la stessa validation.
#     Hint: `field_name: type | None = None` + use `model_dump(exclude_unset=True)`
#
# E6) Test ReDoS:
#     Modifica il pattern username in r"^(a+)+$".
#     Prova UserCreate(username="a"*30 + "!", ...)
#     Misura il tempo. → backtracking esponenziale.
#     Confronta con il pattern originale.
#
# =====================================================================
# DOMANDE DI VERIFICA
# =====================================================================
#
# Q1: Differenza tra validation, sanitization, encoding?
# Q2: Perché whitelist > blacklist?
# Q3: Cos'è ReDoS? Come si previene?
# Q4: Perché bleach con `tags=ALLOWED_TAGS` è meglio di string replace?
# Q5: Cosa fa Pydantic se mandi un campo extra non dichiarato?
# Q6: Differenza tra `model_dump()` e `model_dump(exclude_unset=True)`?
# Q7: Quale tipo di attacco previene `additionalProperties: False` in JSON Schema?
