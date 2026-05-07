# Modulo M5 — Security & Privacy by Design

**Dispensa Tecnica — Corso ITS Cybersecurity (32h)**
**Modulo 5 — 3 ore (2h teoria + 1h workshop)**
**Prerequisiti**: M1 (CIA Triad), M4 (GDPR Art. 25)

---

## Indice

- [Capitolo 1 — Perché "Security by Design"](#cap1)
- [Capitolo 2 — Threat Modeling: il metodo](#cap2)
- [Capitolo 3 — STRIDE: il framework di Microsoft](#cap3)
- [Capitolo 4 — Data Flow Diagram e Trust Boundary](#cap4)
- [Capitolo 5 — Privacy by Design: i 7 principi di Cavoukian](#cap5)
- [Capitolo 6 — Data Minimization in pratica](#cap6)
- [Capitolo 7 — Pseudonimizzazione vs Anonimizzazione](#cap7)
- [Capitolo 8 — DPIA in pillole](#cap8)
- [Capitolo 9 — Workshop: STRIDE su BancaPiccola](#cap9)
- [Capitolo 10 — Sintesi e checklist](#cap10)

---

<a name="cap1"></a>
## Capitolo 1 — Perché "Security by Design"

> Quanto ci vorrà: 20 minuti.

### 1.1 La differenza che cambia tutto

Esistono due modi di costruire un'applicazione:

**Modo A — "metto la sicurezza dopo"**
1. Definisco i requisiti funzionali ("l'utente deve poter fare X")
2. Disegno l'architettura
3. Scrivo il codice
4. Faccio i test funzionali
5. *Spedisco*
6. **Aggiungo la sicurezza** quando il primo cliente segnala un breach

**Modo B — "Security by Design"**
1. Definisco i requisiti funzionali **e di sicurezza** insieme ("l'utente deve poter fare X **senza poter fare Y**")
2. Disegno l'architettura **applicando i 5 principi del secure coding** (M1) **e facendo threat modeling** (questo modulo)
3. Scrivo il codice **rispettando i pattern sicuri**
4. Faccio test funzionali **e test di sicurezza**
5. Spedisco
6. Mantengo la sicurezza nel tempo

### 1.2 Il costo dell'aggiungere dopo

C'è una statistica che gira da decenni nei rapporti IBM, NIST e altri:

| Quando si trova un bug di sicurezza | Costo medio per fix |
|--------------------------------------|---------------------|
| In fase di **requirements/design** | 1× |
| In fase di **coding** | 5× |
| In fase di **testing/QA** | 10× |
| In **produzione** | **100×** |

I numeri esatti variano, ma il pattern è solido: **ogni stadio successivo costa un ordine di grandezza in più**. Trovare una falla a design costa 1, trovarla in produzione costa 100.

E "costo" non è solo denaro: è anche tempo, reputazione, downtime, multe (vedi GDPR/NIS2 di M4).

### 1.3 Lo "Shift Left"

C'è un'espressione che senti continuamente in cybersecurity: **shift left**.

Immagina la pipeline di sviluppo come una linea da sinistra (idea → design → code → test → produzione → operations) a destra. "Shift left" significa **spostare la sicurezza il più a sinistra possibile**, cioè il più presto possibile nel ciclo.

```
[Idea]──[Design]──[Code]──[Test]──[Deploy]──[Run]
   ↑       ↑
   └───────┴─── shift left: la security entra qui
```

In pratica vuol dire:

- **Threat modeling** prima di scrivere codice (questo modulo).
- **Linter di sicurezza** mentre scrivi (es. `bandit` per Python).
- **Static analysis** in CI (es. SonarQube, Snyk Code).
- **Dependency scanning** automatico (es. `pip-audit`, Dependabot).
- **DAST** (test dinamici) prima di andare in produzione.

L'opposto si chiama "shift right" ed è ciò che facevano tutti negli anni '90: aspettare che qualcuno trovi le vulnerabilità *dopo* il rilascio. Non funzionava allora, non funziona oggi.

### 1.4 Caso reale: Equifax 2017

A marzo 2017 viene pubblicata una patch per Apache Struts (CVE-2017-5638, CVSS 10.0).

Equifax la installa? **No**. Per due mesi.

Tra il 13 maggio e il 30 luglio 2017, attaccanti sfruttano la vulnerabilità e rubano dati di **147 milioni di persone** (nomi, SSN, date di nascita, indirizzi).

Costo finale per Equifax:
- ~$1,4 miliardi tra multe e settlements
- Crollo del titolo in borsa (-30%)
- CEO, CSO, CIO licenziati

Una patch installata in tempo avrebbe risolto. Non è successo perché:
1. Non c'era inventario centrale delle dipendenze (no SBOM).
2. Non c'era processo di patching gestito.
3. Non c'era monitoring sufficiente per rilevare l'esfiltrazione.

Tutto questo si decide a **design time**. Non a "ops time".

---

<a name="cap2"></a>
## Capitolo 2 — Threat Modeling: il metodo

> Quanto ci vorrà: 15 minuti.

### 2.1 Cos'è (e cosa non è)

**Threat modeling** è un'attività strutturata in cui ti chiedi: *"cosa potrebbe andare storto in questo sistema, dal punto di vista della sicurezza?"*.

**Non è**:
- Un audit (è prima del codice, l'audit è dopo).
- Un pentest (anche quello è dopo).
- Un'attività one-shot (si rifà a ogni cambio architetturale).
- Roba da specialisti (lo fanno gli sviluppatori, magari con il supporto di un security engineer).

**È**:
- Un'attività di team, fatta a lavagna o su un foglio.
- Strutturata (non a caso): si segue un metodo (STRIDE, PASTA, OCTAVE).
- Iterativa: si aggiorna quando il sistema cambia.

### 2.2 Le 4 domande di Adam Shostack

Adam Shostack (autore di *Threat Modeling: Designing for Security*) propone un framework di **4 domande**, semplici e potenti:

1. **Cosa stiamo costruendo?**
   → Disegna il sistema. Più semplice è il diagramma, meglio è.

2. **Cosa può andare storto?**
   → Applica un framework (es. STRIDE) per elencare minacce.

3. **Cosa facciamo a riguardo?**
   → Per ogni minaccia: la mitighiamo? La accettiamo? La trasferiamo (insurance)? La eliminiamo (cambiamo design)?

4. **Abbiamo fatto un buon lavoro?**
   → Review collettiva. Aggiornamento del modello quando il sistema cambia.

Questo è già un framework completo. Quello che manca è uno **strumento** per fare il punto 2 in modo sistematico. Per quello, c'è **STRIDE**.

---

<a name="cap3"></a>
## Capitolo 3 — STRIDE: il framework di Microsoft

> Quanto ci vorrà: 25 minuti.

### 3.1 Cosa significa STRIDE

STRIDE è stato sviluppato da Microsoft a metà anni '90 (Loren Kohnfelder e Praerit Garg). È un acronimo:

| Lettera | Categoria | Cosa è | Proprietà CIA violata |
|---------|-----------|--------|------------------------|
| **S** | **S**poofing | Fingersi qualcun altro | **Authenticity** |
| **T** | **T**ampering | Modificare dati senza permesso | **Integrity** |
| **R** | **R**epudiation | Negare di aver fatto qualcosa | **Non-repudiation** |
| **I** | **I**nformation Disclosure | Esporre dati che non dovrebbero essere visibili | **Confidentiality** |
| **D** | **D**enial of Service | Rendere il sistema indisponibile | **Availability** |
| **E** | **E**levation of Privilege | Ottenere più privilegi del previsto | **Authorization** |

Ogni categoria si associa a una proprietà di sicurezza. Se un attacco riesce, quella proprietà è violata.

### 3.2 Le 6 categorie con esempi

#### S — Spoofing

L'attaccante si finge un'altra entità (utente, server, app, processo).

**Esempi**:
- Login di un utente con password rubata (l'attaccante "è" l'utente Alice).
- Phishing: email che sembra di una banca ma è dell'attaccante.
- DNS spoofing: il DNS risponde con l'IP dell'attaccante invece che del server vero.
- Certificato TLS contraffatto (mancato controllo da parte del client).

**Difese tipiche**:
- Autenticazione forte (MFA, certificati).
- Protocolli con autenticazione mutua.
- DNSSEC, certificate pinning.

#### T — Tampering

L'attaccante modifica dati o codice senza permesso.

**Esempi**:
- Modifica dei dati in un cookie per simulare un altro utente.
- Modifica di un parametro POST per cambiare il prezzo di un acquisto.
- Modifica del codice di una libreria scaricata (supply chain).
- Modifica di un file su disco a cui ha avuto accesso.

**Difese tipiche**:
- HMAC / firma digitale.
- Integrity check (hash, checksum).
- Validation di input lato server (mai fidarsi del client).
- Filesystem permissions, immutable infrastructure.

#### R — Repudiation

Un utente nega di aver fatto un'azione, e tu non puoi provare il contrario.

**Esempi**:
- "Non ho mai cancellato quel file" (e tu non hai log).
- "Non sono mai stato io a fare quel bonifico" (login non tracciato).
- Modifica del log per nascondere tracce.

**Difese tipiche**:
- Logging robusto (audit trail).
- Log immutabili (es. write-once storage, blockchain in casi estremi).
- Firme digitali sulle azioni critiche.
- Sincronizzazione tempo (NTP) per correlare eventi.

#### I — Information Disclosure

Esposizione di dati che non dovrebbero essere visibili.

**Esempi**:
- SQL Injection che estrae il database (M6).
- Errore 500 che mostra lo stack trace con segreti.
- Endpoint API che restituisce campi sensibili non richiesti.
- File `.env` esposto pubblicamente.
- Backup non cifrato in S3 pubblico.
- Sniffing su HTTP non cifrato (M2).

**Difese tipiche**:
- Cifratura in transito (TLS) e a riposo.
- Error handling che nasconde dettagli.
- Principio del minimo privilegio sui dati.
- Header di sicurezza (M3).
- Configurazione corretta dei cloud (S3 buckets, IAM).

#### D — Denial of Service

Rendere il sistema indisponibile.

**Esempi**:
- DDoS volumetrico (saturare la banda).
- Slowloris (esaurire connessioni TCP).
- Query SQL che blocca il DB.
- Algoritmo con complessità O(n²) su input grande.
- Riempire il filesystem.

**Difese tipiche**:
- Rate limiting.
- WAF / anti-DDoS (Cloudflare, AWS Shield).
- Timeout aggressivi.
- Quote per utente (CPU, storage, request).
- Architettura scalabile.

#### E — Elevation of Privilege

Ottenere privilegi maggiori di quelli concessi.

**Esempi**:
- IDOR (M6.3): da utente normale leggi dati di altri.
- Vulnerabilità nel kernel che da utente passi a root.
- Bypass di un controllo di autorizzazione.
- Privilege escalation dopo SQL Injection (`xp_cmdshell` su SQL Server).

**Difese tipiche**:
- Least privilege rigoroso.
- Controlli di autorizzazione su ogni endpoint (mai solo lato client).
- Separation of duties.
- Audit dei privilegi (chi ha cosa).

### 3.3 STRIDE per elemento

Quando applichi STRIDE su un Data Flow Diagram (vedi cap 4), non tutte le 6 categorie si applicano a tutti gli elementi. Ecco la tabella che usa Microsoft:

| Elemento | S | T | R | I | D | E |
|----------|---|---|---|---|---|---|
| Entità esterna (utente) | ✅ | | ✅ | | | |
| Processo (es. webapp) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Datastore (DB) | | ✅ | | ✅ | ✅ | |
| Flusso (rete) | | ✅ | | ✅ | ✅ | |

Quindi un processo è "vulnerabile a tutto", un flusso "principalmente a Tampering, Disclosure, DoS", ecc. Questa tabella è una **guida** per non dimenticare niente quando fai threat modeling.

### 3.4 Esempio pratico — un form di login

Sistema: form di login web (utente → server → DB users).

**Elementi**:
- Utente (entità esterna)
- Server Flask (processo)
- DB SQLite users (datastore)
- Flusso 1: utente → server (rete HTTPS)
- Flusso 2: server → DB (SQL via libreria)

**Minacce STRIDE per ogni elemento**:

| Elemento | Minaccia STRIDE | Esempio | Difesa |
|----------|-----------------|---------|--------|
| Utente | **S**poofing | Account rubato | MFA, password robuste |
| Utente | **R**epudiation | "Non sono stato io" | Log accessi |
| Server | **S**poofing | Server fake (phishing) | TLS valido + HSTS |
| Server | **T**ampering | Modifica codice in deploy | CI/CD firmata, signed commits |
| Server | **I**nfo disclosure | Stack trace su errore | Error handler generico |
| Server | **D**oS | SYN flood, slow request | Rate limit + WAF |
| Server | **E**levation | SQLi → comandi shell | Query parametrizzate, least privilege DB |
| DB | **T**ampering | Modifica diretta del DB | Permessi filesystem, audit |
| DB | **I**nfo disclosure | Backup non cifrato esposto | Backup cifrato + accesso ristretto |
| Flusso 1 | **I**nfo disclosure | Sniffing su Wi-Fi pubblico | TLS (HTTPS) |
| Flusso 1 | **T**ampering | MITM modifica risposta | TLS + integrity |
| Flusso 2 | **I**nfo disclosure | Cattura traffico DB | TLS sul canale DB, segregazione rete |

Bastano 15 minuti di STRIDE su un sistema semplice per produrre questa lista. Senza STRIDE molte di queste si dimenticano.

---

<a name="cap4"></a>
## Capitolo 4 — Data Flow Diagram e Trust Boundary

> Quanto ci vorrà: 25 minuti.

### 4.1 Il Data Flow Diagram (DFD)

Un DFD è un disegno semplice del tuo sistema. Ha solo **4 simboli**:

| Simbolo | Cosa rappresenta |
|---------|------------------|
| **Rettangolo** | Entità esterna (utente, sistema esterno) |
| **Cerchio** (o tondo) | Processo (codice che fa qualcosa) |
| **Due linee parallele** | Datastore (DB, file, cache) |
| **Freccia** | Flusso di dati |

Un DFD non parla di tecnologia. Non c'è "Flask" o "PostgreSQL" — c'è "webapp" e "DB users". È un'astrazione **logica**, fatta apposta per pensare in termini di sicurezza.

### 4.2 Il Trust Boundary

È il concetto più importante di un DFD per il threat modeling.

> Un **trust boundary** è una linea immaginaria che separa due zone con livelli di fiducia diversi.

Esempi di trust boundary:

- **Internet ↔ tuo server**: tutto ciò che arriva da Internet è "untrusted".
- **Webapp ↔ DB**: la webapp si fida del DB? Il DB si fida della webapp?
- **Browser ↔ JavaScript**: JS che gira nel browser dell'utente è untrusted (l'utente può modificarlo).
- **Container ↔ host**: il container è isolato dall'host?

**Regola**: ogni volta che un dato attraversa un trust boundary, è una **opportunità di attacco**. Lì serve validazione, autenticazione, cifratura, o tutte e tre.

### 4.3 Esempio: DFD di BancaPiccola (versione semplificata)

```
+------------------+                                 +------------------+
|  Utente          |                                 |  DB users        |
|  (entità esterna)|                                 |  (datastore)     |
+--------+---------+                                 +--------+---------+
         |                                                    ^
         | (1) HTTP request                                   | (4) SQL query
         |                                                    |
         v                                                    |
====================== TRUST BOUNDARY: Internet ==============
         |
         v
+------------------+         (3) chiama         +------------------+
|  Login           +--------------------------->+  Auth Service    |
|  (processo Flask)|                            |  (processo)      |
+--------+---------+                            +--------+---------+
         |                                               |
         | (2) HTTP response                             | (4) query/check
         v                                               v
+------------------+                            +------------------+
|  Browser         |                            |  DB users        |
|  (JS lato client)|                            |  (datastore)     |
+------------------+                            +------------------+

====================== TRUST BOUNDARY: server-DB ==============
                                                         |
                                                         v
                                                +------------------+
                                                |  DB sessions     |
                                                |  (datastore)     |
                                                +------------------+
```

**Cosa puoi vedere subito**:

- Il flusso (1) attraversa Internet → **untrusted** → serve TLS + validazione lato server.
- Il flusso (4) attraversa il boundary server↔DB → almeno least privilege e idealmente TLS sul canale.
- Il "browser/JS" è dietro un boundary fiducia (l'utente può modificarlo) → mai fidarsi della validation lato client da sola.

### 4.4 Come si fa un DFD in pratica

Procedura in **5 minuti** per un sistema medio:

1. Disegna le **entità esterne** (chi parla con il sistema).
2. Disegna i **processi principali** (max 5-7 per la prima passata).
3. Disegna i **datastore** che usano i processi.
4. Collega con **frecce** (flussi di dati).
5. Disegna i **trust boundary** (linee tratteggiate).

Strumenti:
- **Lavagna o foglio** (sufficienti).
- **draw.io** (gratuito, online).
- **Microsoft Threat Modeling Tool** (gratuito, integra STRIDE automaticamente).
- **OWASP Threat Dragon** (gratuito, open-source).

---

<a name="cap5"></a>
## Capitolo 5 — Privacy by Design: i 7 principi di Cavoukian

> Quanto ci vorrà: 20 minuti.

### 5.1 Da dove vengono i 7 principi

Ann Cavoukian, già Information & Privacy Commissioner dell'Ontario, formulò i **7 principi della Privacy by Design** nel 2009. Sono diventati la base concettuale di:

- **GDPR Art. 25** — "Privacy by design and by default" (vedi M4).
- ISO/IEC 29100 (Privacy framework).
- NIST Privacy Framework.

Conoscerli non è opzionale: il GDPR li richiede *implicitamente* a chi progetta software che tratta dati personali.

### 5.2 I 7 principi

#### 1. Proactive not Reactive — Preventive not Remedial

Anticipare i problemi di privacy invece di reagirvi dopo.

**Esempio**: durante il design di un form, ti chiedi *"questo campo serve davvero?"* prima di metterlo. Non aspetti che il Garante ti dica di toglierlo.

#### 2. Privacy as the Default Setting

I default devono essere **i più protettivi**. Se l'utente non fa niente, deve essere protetto al massimo.

**Esempio**: una piattaforma social pubblica per default i post solo agli amici, non a tutto il mondo. L'utente deve agire **per pubblicare di più**, non per pubblicare di meno.

**Anti-esempio**: opzione di tracciamento attivata di default, l'utente deve disattivarla. Violazione di GDPR Art. 25.

#### 3. Privacy Embedded into Design

La privacy non è un livello sopra: è dentro l'architettura.

**Esempio**: cifratura end-to-end di Signal, dove neanche il server può leggere i messaggi. Non è "aggiunta": è il *cuore* del design.

#### 4. Full Functionality — Positive-Sum, not Zero-Sum

La privacy non deve essere a scapito della funzionalità. Si può avere entrambe.

**Esempio**: differential privacy in statistiche aggregate — pubblichi statistiche utili senza esporre individui.

**Falso dilemma da evitare**: "Se vuoi privacy devi rinunciare a X". Quasi sempre c'è un design che dà entrambe.

#### 5. End-to-End Security — Lifecycle Protection

Proteggere i dati dall'inizio alla fine: raccolta, uso, archiviazione, cancellazione.

**Esempio**: dati cifrati in transito (TLS), a riposo (DB cifrato), e cancellati in modo verificabile (non solo `DELETE FROM`, anche scrub fisico). Una catena è forte quanto il suo anello più debole.

#### 6. Visibility and Transparency — Keep it Open

Il sistema deve essere verificabile. Le persone devono poter capire cosa fai con i loro dati.

**Esempio**: privacy policy chiara, leggibile (non legalese di 50 pagine). Diritti dell'interessato facilmente esercitabili (export, cancellazione, modifica).

#### 7. Respect for User Privacy — Keep it User-Centric

Mettere l'utente al centro: dati suoi, controllo suo.

**Esempio**: lasciare all'utente di decidere quali dati condividere, con chi, per quanto tempo. Dare strumenti facili per esercitare i diritti GDPR (Artt. 15-22).

### 5.3 Riassunto pratico

| Principio | In una parola |
|-----------|---------------|
| 1. Proactive | Anticipa |
| 2. Default | Proteggi di default |
| 3. Embedded | Architettura |
| 4. Full Functionality | Non zero-sum |
| 5. End-to-End | Tutto il ciclo |
| 6. Transparency | Trasparenza |
| 7. User-Centric | Utente al centro |

---

<a name="cap6"></a>
## Capitolo 6 — Data Minimization in pratica

> Quanto ci vorrà: 15 minuti.

### 6.1 Il principio

GDPR Art. 5(1)(c): i dati devono essere **adeguati, pertinenti e limitati a quanto necessario** rispetto alle finalità.

In una parola: **raccogli il meno possibile**. Non "non raccogliere niente": raccogli quello che ti serve davvero, non un campo in più.

### 6.2 Esempio — form di iscrizione

**Versione "maximalist" (tipica, sbagliata)**:
```
Iscriviti a NewsletterApp:
- Nome
- Cognome
- Email
- Numero di telefono
- Indirizzo completo
- Data di nascita
- Sesso
- Professione
- Reddito annuo
- Consenso marketing (preselezionato)
```

**Versione "minimalist" (corretta)**:
```
Iscriviti a NewsletterApp:
- Email
- (opzionale) Nome (per personalizzare il saluto)
```

Stop. Tutto il resto è invasivo, non serve, e ti espone a obblighi GDPR (giustificazione finalità, conservazione, cancellazione, breach notification se compromessi).

### 6.3 Domande da farsi a design time

Per ogni campo che vuoi raccogliere:

1. **Mi serve davvero?** Se no, non lo raccolgo.
2. **Mi serve per la funzionalità o "potrebbe servire un giorno"?** Se è il secondo: non lo raccolgo.
3. **Mi serve in chiaro?** O posso lavorare con un hash? (Es: per identificare un utente che torna, basta un cookie, non l'email.)
4. **Mi serve per quanto tempo?** Definisci una **retention period** e cancella automaticamente dopo.
5. **A chi serve?** Se a una sola funzionalità di una sola pagina, isolalo lì. Non metterlo nel modello centrale.

### 6.4 Tecniche di minimizzazione

- **Email → hash dell'email**: se devi solo riconoscere "stesso utente", hashing.
- **Data di nascita → fascia d'età**: se ti serve solo per personalizzare (es. "contenuti per >18"), salva "adulto/minore", non la data.
- **Indirizzo → CAP**: se ti serve solo per logistica generale, basta il CAP.
- **Foto → embedding**: per riconoscimento facciale aggregato, ML embedding non reversibile.

### 6.5 Anti-pattern: "raccogli tutto, poi vediamo"

> "Raccogliamo tutto in un data lake, poi i data scientist troveranno qualcosa di utile."

**No.** Questo è esattamente il pattern che il GDPR vuole eliminare. È costoso, è rischioso, è illegale (in UE).

Se i data scientist trovano qualcosa di utile, devono *prima* dichiarare la finalità, *poi* raccogliere il minimo necessario per quella finalità.

---

<a name="cap7"></a>
## Capitolo 7 — Pseudonimizzazione vs Anonimizzazione

> Quanto ci vorrà: 15 minuti.

Sono due tecniche **diverse**. Confondersi è un errore frequente. Per il GDPR, la differenza è enorme:

- **Pseudonimizzato** = ancora dato personale, GDPR si applica.
- **Anonimizzato** = non più dato personale, GDPR **non** si applica.

### 7.1 Pseudonimizzazione

I dati identificativi sono sostituiti da un identificatore artificiale (pseudonimo), ma **esiste una mappa di reidentificazione** tenuta separata.

**Esempio**: nella tabella ordini sostituisci `email` con `user_id = 7438`. Da qualche parte hai una tabella `users(user_id, email)` che lega 7438 a `mario.rossi@example.com`.

**Implicazioni**:
- ✅ Riduce il rischio (un attaccante che prende solo "ordini" non ha email).
- ❌ Non è anonimato: con la mappa puoi reidentificare.
- ⚠️ GDPR si applica ancora.

**Tecniche**:
- Sostituzione con ID artificiale.
- Tokenization.
- Cifratura reversibile con chiave separata.

### 7.2 Anonimizzazione

I dati **non** possono più essere ricondotti a una persona, in modo **irreversibile**, anche con dati esterni.

**Esempio**: pubblichi statistiche aggregate "il 35% degli utenti ha tra i 25 e i 34 anni". Non c'è modo di risalire al singolo individuo.

**Implicazioni**:
- ✅ GDPR non si applica.
- ❌ È molto più difficile di quanto sembri (vedi sotto).

**Tecniche**:
- **Aggregazione**: solo statistiche di gruppi ≥ N persone (k-anonymity).
- **Generalizzazione**: età 27 → "fascia 25-34".
- **Soppressione**: rimuovi righe con valori troppo unici.
- **Differential privacy**: aggiungi rumore matematicamente controllato.
- **Hashing irreversibile** (con cautela: vedi sotto).

### 7.3 La trappola del "credo di aver anonimizzato"

L'anonimizzazione è **molto più difficile di quanto sembri** per due motivi:

#### a) Re-identification con dati esterni

Caso storico: Netflix Prize 2006. Netflix pubblicò un dataset di rating "anonimizzato". Ricercatori (Narayanan, Shmatikov) lo incrociarono con IMDb e re-identificarono singoli utenti dalle loro recensioni pubbliche su entrambe le piattaforme.

#### b) Hash non basta

`hash(email)` **non** è anonimizzazione: se conosci l'email, puoi calcolare l'hash e cercarlo. Per essere veramente irreversibile servono salt, k-anonymity, o differential privacy.

#### c) k-anonymity

Un dataset è "k-anonimo" se ogni individuo non si distingue da almeno k-1 altri. Esempio: se nel tuo dataset c'è "donna, 27 anni, CAP 50100", e in tutto il dataset ci sono altre 4 persone con la stessa combinazione → 5-anonimato. Sotto k=5 di solito non si parla di anonymity vero.

### 7.4 Tabella riassuntiva

| Aspetto | Pseudonimizzazione | Anonimizzazione |
|---------|--------------------|------------------| 
| Reversibile? | Sì (con la mappa) | No |
| GDPR si applica? | Sì | No |
| Difficoltà | Bassa-Media | Alta |
| Quando si usa? | Riduzione rischio interno, lavoro su dati di test | Pubblicazione statistiche, dataset di ricerca |

**Conseguenza pratica**: nel 90% dei casi quello che ti serve è la **pseudonimizzazione**, non la vera anonimizzazione.

---

<a name="cap8"></a>
## Capitolo 8 — DPIA in pillole

> Quanto ci vorrà: 15 minuti.

### 8.1 Cos'è una DPIA

**DPIA — Data Protection Impact Assessment** (Valutazione d'Impatto sulla Protezione dei Dati). È un processo formale che il GDPR (Art. 35) richiede in alcuni casi prima di iniziare un trattamento.

In pratica: un documento che dice "stiamo per fare X con questi dati, abbiamo valutato i rischi, abbiamo le difese pronte".

### 8.2 Quando è obbligatoria

GDPR Art. 35(3) — quando il trattamento può presentare un rischio elevato. Casi tipici:

- Profilazione automatizzata con effetti giuridici sull'individuo.
- Trattamento di **categorie particolari** di dati (Art. 9: salute, etnia, opinioni politiche, biometrici, ecc.) **su larga scala**.
- Sorveglianza sistematica di aree pubbliche (es. videosorveglianza).
- Lista nera del Garante Italiano (es. uso di IoT in domotica con dati salute, monitoraggio dipendenti).

In dubbio? **Falla**. Vale come due viti in più sul progetto.

### 8.3 Cosa contiene (template minimo)

Un mini-template DPIA in 1 pagina:

```markdown
# DPIA — [Nome Trattamento]

Data: [YYYY-MM-DD]
Responsabile: [Nome DPO o equivalente]
Versione: 1.0

## 1. Descrizione
Cosa stiamo facendo? Quali dati? Come?
[2-3 paragrafi]

## 2. Necessità e proporzionalità
Perché lo facciamo? È strettamente necessario?
Le finalità giustificano i dati raccolti?
[Sì/No con motivazione]

## 3. Rischi per gli interessati
- Rischio 1: descrizione, probabilità (bassa/media/alta), impatto (basso/medio/alto)
- Rischio 2: ...
- Rischio 3: ...

## 4. Misure di sicurezza
- Cifratura: [Sì/No, dettagli]
- Pseudonimizzazione: [Sì/No]
- Controllo accessi: [dettagli]
- Audit/logging: [dettagli]
- Retention: [periodo + cancellazione automatica]

## 5. Conclusione
Rischio residuo: [accettabile/non accettabile]
Approvazione DPO: [firma/data]
Rivedere entro: [data]
```

### 8.4 Chi la fa

- **Titolare del trattamento** (in genere l'azienda) → responsabilità.
- **DPO** (Data Protection Officer) → coordina e firma.
- **Sviluppo / Architettura** → fornisce i dettagli tecnici.
- **Legal** → verifica gli aspetti normativi.

In aziende piccole il "team" può essere 1-2 persone con un consulente legale esterno.

### 8.5 Caso pratico

**Scenario**: BancaPiccola decide di aggiungere un sistema di "scoring affidabilità" automatico per concedere prestiti. Il sistema legge dati transazionali e produce un punteggio.

**DPIA obbligatoria?** Sì, perché:
- Profilazione automatizzata.
- Effetti giuridici (concessione/negazione prestito).
- Categoria di dati: finanziari (sensibili, anche se non Art. 9).

**Cosa metterebbe nella DPIA**:
- Logica del modello (anche se è ML).
- Dati usati e perché.
- Diritto di intervento umano (Art. 22 GDPR).
- Trasparenza verso il cliente (cosa vede, può contestare?).
- Misure tecniche (cifratura, audit).
- Bias check (il modello discrimina per genere/etnia? Test).

---

<a name="cap9"></a>
## Capitolo 9 — Workshop: STRIDE su BancaPiccola

> Quanto ci vorrà: 45 min lavoro + 15 min discussione.

### 9.1 Setup

**Gruppi**: 3 persone. **Materiale per ogni gruppo**:

- 1 foglio A3 o lavagna.
- Pennarelli.
- Template `02_lab/M5_lab_stride_template.md` (sotto).

### 9.2 Sistema sotto analisi

BancaPiccola, versione semplificata:

- **Frontend**: pagine HTML rese da Flask (template Jinja2).
- **Backend**: Flask, Python 3.12, gira su un server.
- **DB**: SQLite, file `bancapiccola.db`.
- **Funzionalità**:
  - Login utente (email + password).
  - Dashboard con saldo conto.
  - Lista fatture (`/fatture`).
  - Dettaglio fattura (`/fattura/<id>`).
  - Bonifico (`/bonifico` POST).
  - Upload allegato (`/upload` POST).
  - Download allegato (`/download?file=<nome>`).

### 9.3 Consegna

#### Fase 1 — DFD (15 min)

Disegnate il DFD. Almeno:
- 1 entità esterna (utente)
- 4-5 processi
- 1-2 datastore
- 5-7 flussi
- **2 trust boundary** (almeno: Internet→server, server→DB)

#### Fase 2 — STRIDE (25 min)

Per ogni elemento del DFD, identificate **almeno 2 minacce STRIDE** e proponete **una difesa per ognuna**.

**Riempire la tabella**:

| # | Elemento | Minaccia STRIDE | Descrizione | Difesa |
|---|----------|------------------|-------------|--------|
| 1 | Login (processo) | S — Spoofing | Account rubato | MFA + password robuste |
| 2 | Login (processo) | E — Elevation | Login bypass via SQLi | Query parametrizzate |
| 3 | Lista fatture | E — Elevation | IDOR | Ownership check server-side |
| 4 | DB | I — Disclosure | Backup non cifrato | Cifratura backup |
| ... | ... | ... | ... | ... |

Target: almeno **15 righe** nella tabella.

#### Fase 3 — Priorità (5 min)

Ordinate le minacce per **rischio** (probabilità × impatto, scala 1-5). Quali sono le top 3 da risolvere subito?

### 9.4 Discussione collettiva (15 min)

Ogni gruppo presenta:
- 1 minaccia "ovvia" che ha trovato.
- 1 minaccia "sorprendente" che non avrebbe pensato senza STRIDE.
- 1 difesa che richiede un cambiamento architetturale (non solo "una riga di codice").

Il docente sintetizza alla lavagna i pattern ricorrenti e collega a M6.

### 9.5 Output (consegna)

Tabella STRIDE compilata. Vale come parte di **V2** (peso ~30% di V2).

---

<a name="cap10"></a>
## Capitolo 10 — Sintesi e checklist

### 10.1 Cosa devi sapere alla fine di M5

- ✅ Differenza tra "metto la sicurezza dopo" e "Security by Design".
- ✅ Le 4 domande di Shostack.
- ✅ Le 6 categorie STRIDE con un esempio per ognuna.
- ✅ Disegnare un DFD con processi, datastore, flussi e trust boundary.
- ✅ I 7 principi di Cavoukian.
- ✅ Differenza tra pseudonimizzazione e anonimizzazione (e che la seconda è difficile).
- ✅ Cosa è una DPIA, quando è obbligatoria, cosa contiene.
- ✅ Aver fatto un threat modeling completo su BancaPiccola.

### 10.2 Errori frequenti

- ❌ Pensare che "il pentest finale" sostituisca il threat modeling. No: il pentest è dopo, e trova solo cose che il threat modeling non aveva pensato.
- ❌ Confondere security e privacy. Sovrapposte ma distinte. *Security senza privacy*: la NSA che intercetta tutti i tuoi dati ma li tiene al sicuro. *Privacy senza security*: la lettera anonima che si perde per strada.
- ❌ Pensare che basti "MD5 sull'email" per anonimizzare. **No**, l'email si trova con un dizionario in 5 minuti.
- ❌ Saltare la DPIA pensando "tanto è formalità burocratica". È un esercizio sano: ti costringe a pensare prima di fare.

### 10.3 Per approfondire

- Adam Shostack, *Threat Modeling: Designing for Security* (libro pratico).
- OWASP Threat Modeling Project.
- Microsoft Threat Modeling Tool (gratuito).
- ENISA, *Pseudonymisation Techniques and Best Practices* (PDF gratuito).
- Garante Italiano, [Linee guida DPIA](https://www.garanteprivacy.it).

---

**Prossimo modulo**: M6 — Sicurezza delle Applicazioni Web (9h). Dopo aver visto come **pensare** alla sicurezza, ora vediamo come **scrivere** codice sicuro. Si parte da SQL Injection.
