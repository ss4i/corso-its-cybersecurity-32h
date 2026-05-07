# Modulo M7 — Lab Integrato + Chiusura Corso

**Dispensa Tecnica — Corso ITS Cybersecurity (32h)**
**Modulo 7 — 2 ore (briefing + lavoro + discussione)**
**Prerequisiti**: tutti i moduli precedenti (M0-M6)

> Questo materiale è **operativo**: contiene il briefing per gli studenti, il cheat-sheet di campo, la griglia di valutazione, e la lista delle vulnerabilità presenti in BancaPiccola-vuln (per il docente, da non distribuire prima della consegna).

---

## Indice

- [Capitolo 1 — Briefing per lo studente](#cap1)
- [Capitolo 2 — Cheat-sheet di campo](#cap2)
- [Capitolo 3 — Template del report](#cap3)
- [Capitolo 4 — Griglia di valutazione](#cap4)
- [Capitolo 5 — Per il docente: vulnerabilità presenti in BancaPiccola-vuln](#cap5)
- [Capitolo 6 — Chiusura corso](#cap6)

---

<a name="cap1"></a>
## Capitolo 1 — Briefing per lo studente

> Da leggere ad alta voce in classe a inizio lab (~15 minuti).

### 1.1 Dove sei arrivato

In **30 ore** hai imparato:

1. Cos'è la cybersecurity, la CIA Triad, le minacce principali (M1).
2. Come funziona la rete da 0 a 7 livelli, e dove si attacca (M2).
3. Come funziona HTTP e quali header proteggono (M3).
4. Quali leggi (GDPR, NIS 2, CRA) regolano il tuo lavoro (M4).
5. Come si progetta sicuro fin dall'inizio con STRIDE e Privacy by Design (M5).
6. Come riconoscere e correggere SQL Injection, IDOR, password deboli, XSS, supply chain, path traversal (M6).

### 1.2 Cosa farai nelle prossime 2 ore

Il **lab integrato** è simile a quello che fa un professionista alle prime esperienze: ti viene data un'app e devi fare una **mini-revisione di sicurezza**.

**Scenario fittizio**:

> Sei stato chiamato come junior security analyst da una piccola banca digitale italiana, "**BancaPiccola**". Hanno appena terminato lo sviluppo del nuovo portale clienti e prima del lancio vogliono una review.
> Hai a disposizione il codice sorgente (`BancaPiccola-vuln/`) e un'istanza dell'app che gira in locale.
> **Trova le vulnerabilità, dimostrale, proponi i fix**. Tempo: 75 minuti.

### 1.3 Regole

✅ **Permesso**:

- Leggere il codice sorgente (è una review, non un CTF cieco).
- Usare DevTools, `curl`, `requests`, `sqlite3`, qualunque tool del corso.
- Lavorare a **coppie** (ma report individuali).
- Chiedere **1 hint** al docente. Il secondo hint costa -5% sul voto.
- Consultare le tue dispense e i tuoi appunti.

🚫 **Non permesso**:

- Aprire `BancaPiccola-secure/` prima della consegna.
- Cercare su Google "BancaPiccola vulnerabilities".
- Usare ChatGPT/IA per la soluzione (la metodologia per *cercare* sì — la soluzione no).
- Copiare report (ovvio).

### 1.4 Output richiesto

Un file `cognome_nome_M7_report.md` (o `.docx`/`.pdf`) con almeno **3 vulnerabilità** documentate. Il template completo è nel **cap 3**.

### 1.5 Tempistica

| Tempo | Attività |
|-------|----------|
| 0:00 - 0:15 | Briefing (questo) |
| 0:15 - 1:30 | **Lavoro individuale/a coppie** |
| 1:30 - 1:50 | Discussione collettiva (ognuno presenta UNA vulnerabilità) |
| 1:50 - 2:00 | Chiusura corso |

**Suggerimento di pacing per il discente**:

```
T+0      Setup: clona, installa, avvia bancapiccola-vuln
T+10     Leggi app.py e templates/. Annota i punti sospetti.
T+25     Inizia a testare: login, /fattura/<id>, /download, /upload
T+50     Hai trovato almeno 2 vulnerabilità? Bene. Continua.
T+60     Ne hai trovate 3? Inizia a scrivere il report.
T+75     Aggiungi i fix. Stai per finire.
T+85     Rileggi e consegna.
```

---

<a name="cap2"></a>
## Capitolo 2 — Cheat-sheet di campo

> Distribuito agli studenti **a inizio lab** (cartaceo o stampabile da `02_lab/M7_cheatsheet.md`).

### 2.1 Le 5 vulnerabilità del corso (riassunto)

| # | Vulnerabilità | Dove cercare | Test rapido |
|---|---------------|--------------|-------------|
| 1 | **SQL Injection** | Form di login, ricerca, qualunque input che finisce in WHERE | `' OR '1'='1` ; `' OR 1=1 --` |
| 2 | **IDOR** | URL con ID numerici (`/fattura/42`, `/profilo/3`) | Cambia l'ID |
| 3 | **XSS** | Campi che vengono rivisualizzati (commenti, profilo, ricerca) | `<script>alert(1)</script>` |
| 4 | **Crypto Failures** | Apri il DB con DB Browser. Le password sono in chiaro/MD5/bcrypt? | Visivo |
| 5 | **Path Traversal** | Endpoint con parametro filename | `?file=../etc/passwd` |

### 2.2 "Bonus" da cercare per fare bella figura

| # | Bonus | Dove |
|---|-------|------|
| 6 | **Cookie senza HttpOnly/Secure/SameSite** | DevTools → Application → Cookies |
| 7 | **Header di sicurezza mancanti** | DevTools → Network → guarda risposte |
| 8 | **CVE in dipendenze** | `pip-audit` su `requirements.txt` |
| 9 | **Stack trace su errore 500** | Provoca un errore (es. /fattura/abc invece di /fattura/42) |
| 10 | **Info disclosure** in JSON di risposta (campi sensibili non necessari) | DevTools Network |

### 2.3 Comandi di emergenza

```bash
# Avvia BancaPiccola-vuln
cd BancaPiccola-vuln
.\.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate       # macOS/Linux
python app.py

# Apri il DB
# Apri "DB Browser for SQLite", File → Open Database → bancapiccola.db

# Test SQLi
curl -X POST http://localhost:5000/login -d "email=admin' OR '1'='1&password=anything"

# Test IDOR (loggato come utente, prova URL altri)
# Prima loggati col browser, poi cambia gli ID

# Test XSS
# Inserisci nei commenti: <script>alert("xss")</script>

# Test path traversal
curl "http://localhost:5000/download?file=../../etc/passwd"

# Pip audit dipendenze
pip-audit -r requirements.txt
```

### 2.4 Severity rapida (per giustificare i livelli)

| Livello | Quando | Esempio |
|---------|--------|---------|
| **Critical** (9-10) | Compromissione completa del sistema, accesso senza authn | SQLi che rivela tutte le password, RCE |
| **High** (7-8.9) | Accesso a dati altrui o privilege escalation | IDOR su risorse sensibili, XSS stored |
| **Medium** (4-6.9) | Info disclosure parziale, attacco con interazione | Stack trace, XSS riflessa, cookie senza HttpOnly |
| **Low** (0.1-3.9) | Configurazione subottimale senza impatto immediato | Header `Server` che rivela versione |

---

<a name="cap3"></a>
## Capitolo 3 — Template del report

> Lo studente compila questo template per ogni vulnerabilità trovata. Minimo 3, raccomandate 5+.

### 3.1 Struttura

```markdown
# Mini Security Review — BancaPiccola

**Reviewer**: [Cognome Nome]
**Data**: [YYYY-MM-DD]
**Oggetto**: BancaPiccola v1.0 (commit/tag se disponibile)
**Tempo speso**: ~75 minuti

---

## Executive Summary

In 2-3 frasi: numero di vulnerabilità trovate, severity più alta, raccomandazione generale.

Esempio:
"In 75 minuti ho identificato 5 vulnerabilità, di cui 2 Critical (SQL Injection sul login, IDOR sulle fatture).
L'app non è pronta al lancio: senza fix delle 2 Critical, qualsiasi attaccante può accedere
a dati di tutti i clienti in pochi minuti. Stimo 3-5 giorni di lavoro per la remediation."

---

## Findings

### F-01 — [Titolo descrittivo della vulnerabilità]

| Campo | Valore |
|-------|--------|
| **Severity** | Critical / High / Medium / Low |
| **CVSS (stima)** | 9.8 (esempio) |
| **Localizzazione** | `app.py` riga 42 — endpoint `/login` |
| **Categoria OWASP** | A03 Injection |
| **CWE** | CWE-89 |
| **Norma violata** | GDPR Art. 32(1)(a) |

**Descrizione**:

(2-3 paragrafi: cos'è, dove si manifesta, perché è una vulnerabilità.)

**Proof of Concept**:

```bash
curl -X POST http://localhost:5000/login \
  -d "email=admin' OR '1'='1&password=anything"
```

Output:
```
HTTP/1.1 302 Found
Location: /dashboard
Set-Cookie: session=...
```

L'attaccante è autenticato come admin senza conoscere la password.

**Impatto**:

- Bypass completo dell'autenticazione.
- Accesso a tutti i dati clienti.
- Potenziale escalation a estrazione completa del DB con UNION SELECT.

**Fix proposto**:

```python
# Versione corretta — usa query parametrizzata
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    pwd = request.form.get("password", "")

    user = db.execute(
        "SELECT id, password FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if user and bcrypt.checkpw(pwd.encode(), user["password"]):
        session["user_id"] = user["id"]
        return redirect("/dashboard")
    return "Email o password errati", 401
```

**Effort di fix**: ~30 minuti per endpoint × N endpoint = ~3h totali.

---

### F-02 — [Prossima vulnerabilità]

(stessa struttura)

---

### F-03 — [Prossima vulnerabilità]

(stessa struttura)

---

## Raccomandazioni generali (oltre i fix puntuali)

Esempi:

1. **Switch da SHA-1 a bcrypt** per tutte le password (M6.4).
2. **Centralizzare error handling**: un solo handler 500 generico, log interno dello stack trace.
3. **Aggiungere security headers** (HSTS, CSP, X-Frame-Options).
4. **Configurare cookie sicuri** (Secure, HttpOnly, SameSite).
5. **Pip-audit in CI**.

---

## Compliance check (cenno)

- **GDPR Art. 32**: NON conforme (password debole, cifratura assente, IDOR).
- Notifica **72h** al Garante necessaria se l'app è in produzione e queste vulnerabilità portano a un breach.

```

### 3.2 Esempio compilato (parziale)

> Per riferimento, ecco come potrebbe apparire un report ben fatto. Distribuibile come esempio ai discenti **DOPO** la consegna.

```markdown
### F-02 — IDOR su dettaglio fattura

| Campo | Valore |
|-------|--------|
| **Severity** | High |
| **CVSS (stima)** | 7.5 (AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N) |
| **Localizzazione** | `app.py` riga 87, endpoint `/fattura/<int:fid>` |
| **Categoria OWASP** | A01 Broken Access Control |
| **CWE** | CWE-639 |
| **Norma violata** | GDPR Art. 5(1)(f), Art. 32 |

**Descrizione**:
L'endpoint `/fattura/<int:fid>` recupera la fattura con ID `fid` dal database e la restituisce al richiedente. **Non c'è alcun controllo che l'utente loggato sia il proprietario della fattura**. Sfruttando questo, un utente autenticato può vedere fatture di altri clienti semplicemente cambiando l'ID nell'URL.

**Proof of Concept**:
1. Login come utente normale (`mario@example.com`).
2. Visita la propria fattura legittima: `http://localhost:5000/fattura/3` → vista.
3. Modifica l'ID: `http://localhost:5000/fattura/7` → vedo la fattura del cliente con ID 7 (Lucia Bianchi, importo 1.234€, IBAN visibile).

**Impatto**: data breach a tutti gli effetti — un utente legittimo accede a dati personali e finanziari di **tutti** gli altri clienti. Con uno script può scaricare l'intero catalogo fatture in pochi minuti.

**Fix proposto**:
```python
@app.route("/fattura/<int:fid>")
@login_required
def fattura(fid):
    f = Fattura.query.filter_by(
        id=fid,
        owner_id=session["user_id"]
    ).first()
    if not f:
        abort(403)  # 403 perché 404 darebbe info sull'esistenza
    return render_template("fattura.html", fattura=f)
```

Anche su `PUT/DELETE` lo stesso controllo va replicato.
```

---

<a name="cap4"></a>
## Capitolo 4 — Griglia di valutazione

> Per il docente. Lab M7 vale il **20% del voto finale**.

### 4.1 Voce per voce (su 100)

| Voce | Peso | Cosa valutare |
|------|------|---------------|
| **Numero vulnerabilità identificate** (≥3) | 20 | 3 = sufficiente, 5+ = ottimo, 2 = parziale (10pt) |
| **Correttezza tecnica delle PoC** | 30 | PoC funziona davvero? È riproducibile? |
| **Qualità dei fix proposti** | 30 | Codice corretto? Idiomatico? Risolve davvero? |
| **Severity giustificata** | 10 | Coerente con l'impatto reale? CVSS plausibile? |
| **Norma/categoria identificata** | 10 | OWASP/CWE/GDPR collegati correttamente? |

### 4.2 Mappatura voto

| Voto | Punti | Descrizione |
|------|-------|-------------|
| **Eccellente** (≥90) | ≥90 | 5+ vuln (incluse 1-2 bonus), fix corretti, severity giustificate, normativa. |
| **Buono** (75-89) | 75-89 | 4-5 vuln, qualche fix migliorabile, mapping corretto. |
| **Sufficiente** (60-74) | 60-74 | 3 vuln (le più ovvie), fix accettabili, almeno mapping OWASP. |
| **Insufficiente** (<60) | <60 | <3 vuln, o fix sbagliati, o nessun mapping. |

### 4.3 Indicatori di "report eccezionale" (lode/eccellenza)

- ✅ Trovato ≥1 vuln "bonus" (cookie, header, supply chain, ecc.)
- ✅ Severity con vector string CVSS plausibile
- ✅ Fix non solo "patch puntuale" ma anche "raccomandazione architetturale"
- ✅ Sezione "Compliance check" con riferimenti a GDPR/NIS2
- ✅ Executive summary chiaro e onesto

### 4.4 Indicatori di "report da correggere"

- ❌ "Ho trovato 3 vulnerabilità" ma sono tutte la stessa cosa.
- ❌ Fix che usa `eval`, `Markup(...)`, `|safe`, o anti-pattern.
- ❌ "Severity Critical" su un cookie senza HttpOnly.
- ❌ Non distingue 401 da 403.
- ❌ Confonde MD5 con bcrypt.

---

<a name="cap5"></a>
## Capitolo 5 — Per il docente: vulnerabilità presenti in BancaPiccola-vuln

> ⚠️ **NON DISTRIBUIRE AGLI STUDENTI PRIMA DELLA CONSEGNA.**
>
> Questo è il "ground truth" del lab integrato.

### 5.1 Vulnerabilità "principali" (le 5 del corso)

#### F-01 — SQL Injection nel login

- **File**: `app.py`
- **Endpoint**: `POST /login`
- **Codice vulnerabile** (atteso): query con f-string o concat su `email` e/o `password`.
- **PoC**: `email=admin' OR '1'='1&password=qualunque`
- **Severity attesa**: Critical (CVSS ~9.8)
- **OWASP**: A03 Injection / CWE-89
- **GDPR**: Art. 32

#### F-02 — IDOR su dettaglio fattura

- **File**: `app.py`
- **Endpoint**: `GET /fattura/<int:fid>`
- **Codice vulnerabile**: manca controllo `owner_id == session["user_id"]`.
- **PoC**: cambia l'ID nell'URL.
- **Severity attesa**: High (CVSS ~7.5)
- **OWASP**: A01 / CWE-639

#### F-03 — Stored XSS nei commenti del profilo

- **File**: `templates/profilo.html`
- **Codice vulnerabile**: `{{ commento | safe }}` o output non escaped.
- **PoC**: inserisci `<script>alert(document.cookie)</script>` come commento, ricaricala pagina, vedi alert.
- **Severity attesa**: High (CVSS ~7.0)
- **OWASP**: A03 / CWE-79

#### F-04 — Password in SHA-1 senza salt

- **File**: `app.py` (logica login/registrazione)
- **Codice vulnerabile**: `hashlib.sha1(pwd.encode()).hexdigest()`.
- **PoC visiva**: aprire `bancapiccola.db` con DB Browser, vedere hash 40 caratteri esadecimali identici per password uguali.
- **Severity attesa**: High (CVSS ~7.5 — combinato con altre vuln diventa Critical)
- **OWASP**: A02 / CWE-916, CWE-328

#### F-05 — Path Traversal nell'endpoint download

- **File**: `app.py`
- **Endpoint**: `GET /download?file=`
- **Codice vulnerabile**: `send_file(f"./uploads/{filename}")` senza validazione.
- **PoC**: `?file=../app.py` (legge codice sorgente), `?file=../bancapiccola.db` (legge DB).
- **Severity attesa**: High (CVSS ~7.5)
- **OWASP**: A01 / CWE-22

### 5.2 Vulnerabilità "bonus"

#### F-06 — Cookie senza HttpOnly/Secure/SameSite

- **File**: configurazione Flask (`app.config`)
- **PoC visiva**: DevTools → Application → Cookies, manca HttpOnly.
- **Severity**: Medium (4-6)

#### F-07 — Header di sicurezza mancanti

- **PoC**: `curl -I http://localhost:5000/`. Mancano HSTS, CSP, X-Frame-Options.
- **Severity**: Medium

#### F-08 — Stack trace su errore (DEBUG=True in produzione)

- **File**: `app.py` ultima riga
- **PoC**: provoca errore (es. `/fattura/abc`), vedi stack trace HTML.
- **Severity**: Medium (info disclosure)

#### F-09 — Supply Chain — CVE in `requirements.txt`

- **File**: `requirements.txt` con versioni vulnerabili (es. `flask==2.0.0`).
- **PoC**: `pip-audit -r requirements.txt`.
- **Severity**: Medium (a seconda della CVE)

#### F-10 — Endpoint `/api/users` espone tutti i campi

- **File**: `app.py`, endpoint API
- **Codice vulnerabile**: `return jsonify(User.query.all())` espone `password_hash`, `is_admin`.
- **Severity**: High

### 5.3 Mappatura sufficienza/eccellenza

| Trovate | Voto |
|---------|------|
| F-01 + F-02 + F-04 (le 3 più grosse) | sufficiente (60-70) |
| 4 di F-01 a F-05 | buono (75-85) |
| Tutte F-01 a F-05 | molto buono (85-90) |
| F-01 a F-05 + ≥2 bonus | eccellente (90-95) |
| Tutte + analisi compliance + raccomandazioni architetturali | lode (95-100) |

### 5.4 Hint che il docente può dare (con costo)

- **Hint 1 gratuito**: "Hai testato i form con caratteri speciali?"
- **Hint 2 (-5%)**: "Hai aperto il database con DB Browser? Cosa vedi nelle password?"
- **Hint 3 (-10%)**: "Hai provato a cambiare gli ID negli URL?"
- **Hint disperato (-20%)**: "Stai cercando in tutti i posti del cheat-sheet di campo?"

---

<a name="cap6"></a>
## Capitolo 6 — Chiusura corso (10 min)

> Da fare in aula al termine della discussione collettiva.

### 6.1 Cosa hai imparato in 32 ore

In modo concreto, da oggi sei in grado di:

1. ✅ Riconoscere e classificare minacce informatiche.
2. ✅ Capire come funziona la rete (ISO/OSI) e dove si attacca.
3. ✅ Leggere e ispezionare richieste HTTP, capire status code e header di sicurezza.
4. ✅ Sapere quali norme regolano il tuo lavoro (GDPR, NIS 2, CRA).
5. ✅ Applicare Threat Modeling (STRIDE) e Privacy by Design.
6. ✅ Riconoscere e correggere le 5 vulnerabilità web più diffuse.
7. ✅ Usare strumenti professionali (Wireshark, DevTools, pip-audit, DB Browser).
8. ✅ Scrivere uno script Python di scanning/sniffing (a fini didattici legali).
9. ✅ Fare una mini security review con report formale.

> Sei al **punto di partenza giusto**. Non sei un penetration tester e non sei un esperto di crittografia, ma hai le **fondamenta** per crescere in qualunque direzione.

### 6.2 I 3 takeaway più importanti

Se devi ricordare 3 cose tra 5 anni:

1. **La sicurezza non è un add-on**. Si progetta dall'inizio (Security & Privacy by Design).
2. **Difese stratificate**. Mai una sola difesa. Mai "tanto ho HTTPS".
3. **Mentalità avversaria**. "Cosa fa il mio codice che non dovrebbe fare?". Più importante della conoscenza tecnica.

### 6.3 Per crescere ancora

#### Risorse gratuite

- **PortSwigger Web Security Academy** (https://portswigger.net/web-security): la migliore risorsa gratuita al mondo per web security. Lab guidati, certificazione finale.
- **TryHackMe** (https://tryhackme.com): rooms guidate, beginner-friendly. Free tier ampio.
- **HackTheBox starting point** (https://www.hackthebox.com): più hard, ma cresci tanto.
- **OverTheWire Bandit** (https://overthewire.org/wargames/bandit/): linux + security, eccellente per principianti.
- **OWASP** (https://owasp.org): documentazione, cheat sheets, tool gratuiti.

#### Certificazioni "entry"

- **CompTIA Security+** (vendor neutral, base). Vale ~150€ e dura ~3 mesi di studio.
- **eJPT — eLearnSecurity Junior Penetration Tester** (più tecnica, hands-on).
- **PortSwigger BSCP** (Burp Suite Certified Practitioner) — molto pratica per chi vuole fare AppSec.

#### Da studiare al II anno ITS

- **Penetration testing pratico** (Kali, Metasploit, Burp Pro)
- **Crittografia avanzata** (algoritmi simmetrici/asimmetrici, hashing, PKI)
- **Cloud security** (AWS/Azure/GCP)
- **Container security** (Docker, Kubernetes)
- **DevSecOps** (security in CI/CD)
- **Forensics e incident response**

### 6.4 Il messaggio finale

> "Sappiamo abbastanza per essere pericolosi" — questo è dove siete arrivati.
>
> Non sappiamo abbastanza per essere maestri. Ma sappiamo abbastanza per **vedere** quando qualcosa non va, e per **chiedere le domande giuste**.
>
> In azienda sarete giovani sviluppatori. Probabilmente nessuno vi chiederà esplicitamente di "fare sicurezza". Sarà compito vostro **dirla**. Quando vedrete una query concatenata, una password in MD5, un endpoint senza authz — spettare a voi alzare la mano.
>
> È noioso? A volte sì. Ma è il lavoro per cui vi pagheranno tra qualche anno, e quello che farà la differenza tra un'app che dura e un'app che finisce sul giornale.
>
> Buona strada.

---

**Fine del corso.**

> *Un grazie a chi è arrivato fino qui. Per dubbi, errori in queste dispense, suggerimenti: parliamone alla prossima lezione.*
