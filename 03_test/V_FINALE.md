# Verifica Finale — Cybersecurity e Sicurezza delle Applicazioni

**Corso:** ITS — 32 ore
**Tutti i moduli:** M0-M7
**Durata:** 90 minuti
**Punteggio totale:** 100

**Cognome e Nome:** _______________________________
**Data:** _________________________________________

---

## Istruzioni

- 4 sezioni: scelta multipla (30 pt), risposta breve (20 pt), code review (30 pt), scenario integrato (20 pt).
- Per le code review: leggi il codice, identifica vulnerabilità, scrivi la versione corretta.
- Tempo gestito autonomamente. Calcolatrici/dispositivi NON ammessi salvo necessità di accessibilità.

---

## Sezione A — Scelta multipla (15 × 2 = 30 punti)

**A1.** Una webapp Flask salva le password con `hashlib.sha1(pwd.encode()).hexdigest()`. Quale problema ha?
- [ ] a) SHA-1 è troppo lento per il mobile
- [ ] b) Manca il salt, e SHA-1 è considerato debole — preferire bcrypt/Argon2id
- [ ] c) hashlib non è disponibile su Windows
- [ ] d) Nessun problema, è una scelta moderna

**A2.** Quale di questi è un esempio di **IDOR**?
- [ ] a) `username=' OR '1'='1` nel form di login
- [ ] b) `<script>alert(1)</script>` in un campo commento
- [ ] c) Modificare l'URL `/fattura/42` in `/fattura/43` per vedere fatture altrui
- [ ] d) Inviare 1 milione di richieste in 1 secondo

**A3.** Il payload `<script>fetch('/api/users')</script>` in un campo commento è un attacco di tipo:
- [ ] a) SQL Injection
- [ ] b) XSS Stored
- [ ] c) CSRF
- [ ] d) Path Traversal

**A4.** Quale linea di codice è **vulnerabile a SQL Injection**?
- [ ] a) `cursor.execute("SELECT * FROM u WHERE id = ?", (user_id,))`
- [ ] b) `cursor.execute(f"SELECT * FROM u WHERE id = {user_id}")`
- [ ] c) `db.session.query(User).filter_by(id=user_id).first()`
- [ ] d) `User.query.get(user_id)`

**A5.** Quale di questi è il modo **corretto** di hashare una password in Python con bcrypt?
- [ ] a) `bcrypt.hashpw(password, "")`
- [ ] b) `bcrypt.hashpw(password.encode(), bcrypt.gensalt())`
- [ ] c) `bcrypt.encrypt(password)`
- [ ] d) `hashlib.bcrypt(password)`

**A6.** Quale tool serve a verificare se le tue dipendenze Python hanno CVE note?
- [ ] a) `pylint`
- [ ] b) `black`
- [ ] c) `pip-audit`
- [ ] d) `mypy`

**A7.** L'attacco "Path Traversal" tipicamente sfrutta:
- [ ] a) `../` per uscire dalla cartella prevista
- [ ] b) JavaScript inline
- [ ] c) Buffer overflow
- [ ] d) Replay di sessione

**A8.** Quale di questi è uno status code HTTP appropriato per "autenticato ma non autorizzato"?
- [ ] a) 401 Unauthorized
- [ ] b) 403 Forbidden
- [ ] c) 404 Not Found
- [ ] d) 500 Internal Server Error

**A9.** Per impedire CSRF, una difesa moderna è:
- [ ] a) `Set-Cookie: SameSite=Strict` o `Lax`
- [ ] b) Usare GET per tutte le operazioni
- [ ] c) Disabilitare i cookie
- [ ] d) Usare HTTP invece di HTTPS

**A10.** Quale linea Jinja2 è vulnerabile a XSS Stored?
- [ ] a) `<p>{{ comment }}</p>`
- [ ] b) `<p>{{ comment | safe }}</p>` quando comment proviene da utente
- [ ] c) `<p>{{ comment | escape }}</p>`
- [ ] d) `<p>{{ comment | e }}</p>`

**A11.** L'attacco SolarWinds (2020) appartiene principalmente a quale categoria?
- [ ] a) DDoS
- [ ] b) Phishing
- [ ] c) Supply Chain
- [ ] d) MITM

**A12.** Per le password in produzione moderna, la scelta ottimale è:
- [ ] a) MD5
- [ ] b) SHA-256 senza salt
- [ ] c) bcrypt o Argon2id
- [ ] d) Base64

**A13.** Una **DPIA** è obbligatoria per:
- [ ] a) Qualunque sito web
- [ ] b) Trattamenti che presentano rischio elevato per gli interessati
- [ ] c) Solo aziende con > 500 dipendenti
- [ ] d) Solo se richiesta dal Garante

**A14.** Lo `Strict-Transport-Security` (HSTS):
- [ ] a) Cifra le password
- [ ] b) Forza il browser a usare HTTPS dopo prima visita
- [ ] c) Blocca i bot
- [ ] d) Sostituisce TLS

**A15.** Quale di queste **NON** è una mitigazione corretta per XSS?
- [ ] a) Escape dell'output (Jinja2 `{{ }}`)
- [ ] b) Content-Security-Policy (CSP)
- [ ] c) Cookie HttpOnly
- [ ] d) Disabilitare gli header di sicurezza

---

## Sezione B — Risposta breve (5 × 4 = 20 punti)

**B1.** *(4 punti)* Cita **3 vulnerabilità della OWASP Top 10:2025** e per ognuna fai un esempio di scenario in cui si manifesta.

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

**B2.** *(4 punti)* Spiega in 4-5 righe **perché MD5 è inadeguato per le password**, e quale alternativa moderna useresti specificando i suoi vantaggi.

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

**B3.** *(4 punti)* Una webapp restituisce 401 sia quando l'utente non esiste, sia quando la password è sbagliata. Perché è una scelta corretta? Cosa eviterebbe **rispondere 404 "utente non esiste" + 401 "password sbagliata"**?

___________________________________________________

___________________________________________________

___________________________________________________

**B4.** *(4 punti)* Cita **3 differenze fra autenticazione e autorizzazione**, con un esempio per ognuna.

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

**B5.** *(4 punti)* Un endpoint `/api/cerca?q=alice` produce in risposta lo stack trace dell'eccezione SQLAlchemy. Quale **categoria STRIDE** è violata? Quale **principio del Secure Coding** è ignorato? Come si corregge?

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

---

## Sezione C — Code review (3 esercizi × 10 punti = 30 punti)

### C1. Login vulnerabile *(10 punti)*

Leggi questo codice Flask:

```python
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    pwd = request.form["password"]

    sql = f"SELECT id, password FROM users WHERE email = '{email}'"
    row = db.execute(sql).fetchone()

    if row and row[1] == hashlib.sha1(pwd.encode()).hexdigest():
        session["user_id"] = row[0]
        return redirect("/dashboard")
    return "Login fallito", 401
```

**Domande**:

1. *(2 pt)* Indica **3 vulnerabilità** distinte presenti nel codice.

   1. _________________________________________________
   2. _________________________________________________
   3. _________________________________________________

2. *(2 pt)* Quale payload nel campo `email` permetterebbe di bypassare il login senza conoscere la password?
   _________________________________________________

3. *(6 pt)* Riscrivi il codice corretto (puoi assumere `bcrypt`, `sqlalchemy`, validazione email):

```python
# Spazio per riscrivere










```

### C2. Endpoint con IDOR *(10 punti)*

```python
@app.route("/fattura/<int:fid>")
def fattura(fid):
    f = Fattura.query.get(fid)
    if not f:
        return "Non trovata", 404
    return render_template("fattura.html", fattura=f)
```

**Domande**:

1. *(3 pt)* Spiega in 2-3 righe la vulnerabilità presente.
   _________________________________________________
   _________________________________________________
   _________________________________________________

2. *(2 pt)* Quale status code restituiresti se l'utente è autenticato ma non è il proprietario della fattura?
   _________________________________________________

3. *(5 pt)* Riscrivi il codice corretto, includendo controllo di autenticazione e ownership:

```python
# Spazio per riscrivere









```

### C3. Endpoint download *(10 punti)*

```python
@app.route("/download")
def download():
    filename = request.args.get("file")
    return send_file(f"./uploads/{filename}")
```

**Domande**:

1. *(2 pt)* Quale vulnerabilità è presente? Come si chiama in OWASP?
   _________________________________________________

2. *(2 pt)* Indica **2 payload** che un attaccante potrebbe usare per leggere file di sistema.
   _________________________________________________
   _________________________________________________

3. *(6 pt)* Riscrivi una versione sicura. Almeno: validazione del nome file, normalizzazione path, controllo che il path finale sia dentro la cartella `uploads`.

```python
# Spazio per riscrivere










```

---

## Sezione D — Scenario integrato (20 punti)

### Scenario

Sei stato chiamato a fare una **revisione architetturale** di un nuovo servizio: `MyDocs`, un'app web (Flask + PostgreSQL) per condividere documenti professionali tra studi legali.

**Caratteristiche del servizio**:
- Login utente con email/password.
- Upload documenti PDF (fino a 50MB).
- Ogni documento ha un proprietario; può essere "condiviso" con altri utenti tramite link `/doc/<uuid>`.
- I documenti sono salvati nel filesystem del server (`/var/myapp/docs/`).
- Le password sono salvate in MD5.
- Il server gira come `root` per "non avere problemi di permessi".
- Non c'è MFA.
- Il certificato HTTPS è scaduto (gestione manuale).
- Cookie di sessione: `Set-Cookie: session=abc123`.
- Backup notturno del DB su S3, bucket pubblico.

### Consegna

**D1.** *(8 pt)* Identifica **almeno 5 vulnerabilità/problemi** di sicurezza, classificandoli secondo la **OWASP Top 10** o un principio del Secure Coding.

| # | Problema identificato | Categoria OWASP / Principio violato |
|---|------------------------|--------------------------------------|
| 1 | _______________________________ | ________________________________ |
| 2 | _______________________________ | ________________________________ |
| 3 | _______________________________ | ________________________________ |
| 4 | _______________________________ | ________________________________ |
| 5 | _______________________________ | ________________________________ |

**D2.** *(4 pt)* Per ognuno dei 5 problemi, indica **livello di severity** (Low/Medium/High/Critical) con **giustificazione di una riga**.

| # | Severity | Giustificazione |
|---|----------|-----------------|
| 1 | __________ | __________________________________ |
| 2 | __________ | __________________________________ |
| 3 | __________ | __________________________________ |
| 4 | __________ | __________________________________ |
| 5 | __________ | __________________________________ |

**D3.** *(4 pt)* Per i **2 problemi più critici**, proponi una **soluzione tecnica concreta** in 1-2 righe.

**Problema #__**: _________________________________
**Soluzione**: ____________________________________
__________________________________________________

**Problema #__**: _________________________________
**Soluzione**: ____________________________________
__________________________________________________

**D4.** *(4 pt)* Indica **almeno 1 articolo del GDPR** e **1 articolo della NIS 2** (se applicabile) potenzialmente violati. Spiega perché.

**GDPR**: Art. ___ — _________________________________

___________________________________________________

**NIS 2**: Art. ___ — _________________________________

___________________________________________________

---

**FINE — Buon lavoro.**

> *Questa è la verifica finale del corso. Insieme al lab integrato M7, determina la valutazione finale.*
