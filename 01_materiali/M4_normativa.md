# Modulo M4 — Quadro Normativo Europeo

**Dispensa Tecnica — Corso ITS Cybersecurity (32h)**
**Modulo 4 — 2 ore (lezione frontale, no lab)**
**Prerequisiti**: M1 (concetti di base CIA Triad)

> **Materiale di riferimento principale**: Capitolo 2 della dispensa `dispensa-sviluppo-sicuro-software.docx`.
> Questo documento integra:
> - Tabella estesa "errore di codice → norma violata"
> - 5 casi italiani reali (provvedimenti Garante)
> - Mini-quiz di autovalutazione
> - Diagramma di flusso "ho un breach: cosa faccio?"

---

## Indice

- [Capitolo 1 — Perché un programmatore deve sapere di leggi](#cap1)
- [Capitolo 2 — GDPR: gli articoli che riguardano il codice](#cap2)
- [Capitolo 3 — NIS 2: chi è "soggetto" e cosa deve fare](#cap3)
- [Capitolo 4 — Cyber Resilience Act (CRA)](#cap4)
- [Capitolo 5 — Tabella errore → norma](#cap5)
- [Capitolo 6 — 5 casi italiani reali](#cap6)
- [Capitolo 7 — Diagramma di flusso post-breach](#cap7)
- [Capitolo 8 — Mini quiz di autovalutazione](#cap8)

---

<a name="cap1"></a>
## Capitolo 1 — Perché un programmatore deve sapere di leggi

> Quanto ci vorrà: 10 minuti.

Tre frasi che senti spesso da chi scrive codice:

> ❌ "Le leggi sono cose da avvocati."
> ❌ "Se sbaglio io, paga l'azienda."
> ❌ "Tanto in Italia non ti beccano."

Tutte e tre **sbagliate**.

### 1.1 Le leggi parlano di **codice**

GDPR Art. 32 cita esplicitamente:

> «Il titolare del trattamento e il responsabile del trattamento mettono in atto **misure tecniche e organizzative adeguate** per garantire un livello di sicurezza adeguato al rischio, che comprendono, tra le altre, se del caso: la pseudonimizzazione e la **cifratura dei dati personali** [...]»

"Misure tecniche" significa **codice e configurazioni**. Non un'attività esterna al lavoro dello sviluppatore.

### 1.2 Le sanzioni colpiscono l'azienda **e** il manager (e talvolta l'individuo)

- **GDPR**: multe fino a 20M€ o 4% fatturato.
- **NIS 2**: fino a 10M€ o 2%, **più responsabilità personale del management** (sospensione dalle funzioni dirigenziali!).
- **CRA**: fino a 15M€ o 2,5%.

Le aziende, dopo un breach, fanno **indagini interne**. Chi ha scritto/firmato cosa? Chi ha approvato la non-patch? Sviluppatori e architetti **vengono interrogati**. In casi gravi, contenziosi con licenziamenti.

### 1.3 In Italia il Garante ispeziona regolarmente

Solo nel **2024** il Garante ha emesso **oltre 100 provvedimenti** con sanzioni che vanno da 5.000€ a oltre 10M€.

Settori toccati: sanità, banche, scuole, comuni, e-commerce, app sportive, transport. **Nessun settore è escluso**.

### 1.4 Conclusione

Conoscere le 3 norme di questo modulo è **competenza professionale** di un developer moderno, non un'extra. Andiamo al sodo.

---

<a name="cap2"></a>
## Capitolo 2 — GDPR: gli articoli che riguardano il codice

> Quanto ci vorrà: 40 minuti.

### 2.1 GDPR — definizione in 3 righe

**GDPR** = Regolamento (UE) 2016/679 — General Data Protection Regulation.
Si applica a chiunque tratti dati personali di residenti UE, ovunque sia stabilita l'azienda.
In vigore dal **25 maggio 2018**.

### 2.2 Cos'è un "dato personale"

GDPR Art. 4(1):

> «"Dato personale": qualsiasi informazione **riguardante una persona fisica identificata o identificabile** [...]»

**Esempi di dato personale**:
- Nome, cognome, codice fiscale, indirizzo
- Email, numero di telefono, IP fissi
- Foto, video, voce
- Cronologia acquisti, geolocalizzazione, comportamento online
- Cookie identificativi (in molti casi)

**Esempi di dato NON personale**:
- "Il 35% degli utenti ha tra i 25 e i 34 anni" (statistica aggregata anonima)
- Codice sorgente di un'app
- Dati di un'azienda (sono dati aziendali, non personali — anche se l'email del CEO sì)

### 2.3 Categorie particolari (Art. 9)

Dati con **protezione rinforzata**:
- Salute (cartelle cliniche, prescrizioni)
- Origine razziale/etnica
- Opinioni politiche, religiose, filosofiche
- Appartenenza sindacale
- Dati genetici e biometrici
- Vita sessuale, orientamento sessuale
- Dati giudiziari

Trattare questi dati richiede **base giuridica rafforzata** (consenso esplicito o casi specifici dell'Art. 9(2)).

### 2.4 Articoli che riguardano direttamente il codice

#### Art. 5 — Principi del trattamento

I dati devono essere trattati nel rispetto di **6 principi**:

| Principio | In una frase | Implicazione tecnica |
|-----------|--------------|----------------------|
| Liceità, correttezza, trasparenza | Tratti dati con base giuridica e l'utente lo sa | Privacy policy chiara, cookie banner conforme |
| Limitazione delle finalità | Dati raccolti per scopi specifici, non altri | Audit "perché stiamo usando questi dati?" |
| **Minimizzazione** | Solo i dati necessari | M5 — Data Minimization. Form snelli. |
| Esattezza | Dati corretti e aggiornati | Endpoint per modifica dati personali |
| Limitazione della conservazione | Conservazione per il tempo necessario | Retention policy + cancellazione automatica |
| **Integrità e riservatezza** | Sicurezza adeguata | Cifratura, controllo accessi, pseudonimizzazione |

#### Art. 25 — Privacy by Design and by Default

> «Il titolare del trattamento mette in atto misure tecniche e organizzative adeguate **al momento di determinare i mezzi del trattamento** [...] per garantire che siano trattati, **per impostazione predefinita, solo i dati personali necessari** [...]»

**Implicazione**: la privacy si progetta **prima di scrivere codice**. Vedi M5.

#### Art. 32 — Sicurezza del trattamento (l'articolo critico per gli sviluppatori)

L'articolo che gli sviluppatori violano più spesso. Cita esplicitamente:

- (a) **Pseudonimizzazione e cifratura** dei dati personali
- (b) **Riservatezza, integrità, disponibilità** e resilienza dei sistemi
- (c) **Capacità di ripristino** dei dati (backup)
- (d) **Procedura di test, verifica e valutazione regolare** delle misure

Tradotto: il GDPR ti dice di:
- Cifrare dati a riposo e in transito (TLS, DB cifrato).
- Pseudonimizzare quando possibile (M5).
- Avere backup funzionanti.
- Fare audit periodici / pentest / vulnerability scan.

**Non rispettare l'Art. 32 = violazione anche senza un breach**.

#### Art. 33 — Notifica del breach al Garante (entro 72 ore)

In caso di **violazione di dati personali** (data breach), il titolare deve **notificare al Garante entro 72 ore** dalla scoperta.

Cosa contiene la notifica:
- Natura della violazione, categorie e numero approssimativo di interessati
- Conseguenze probabili
- Misure adottate o proposte per affrontare la violazione

**72 ore non sono molte**. Se è venerdì sera e scopri un breach domenica mattina, hai fino a mercoledì notte. Bisogna avere un **playbook pronto**.

#### Art. 34 — Comunicazione agli interessati

Se il breach può comportare un **rischio elevato** per gli interessati, devi anche **comunicarlo a loro** (es. via email).

Eccezioni (puoi NON comunicare se):
- I dati erano cifrati e la chiave è al sicuro.
- Hai adottato misure successive che mitigano il rischio.
- La comunicazione richiederebbe sforzi sproporzionati (allora comunicato pubblico).

#### Art. 35 — Data Protection Impact Assessment (DPIA)

Quando un trattamento può presentare **rischio elevato**, serve una DPIA *prima* di iniziare.

Vedi M5 cap 8.

### 2.5 Sanzioni GDPR

| Categoria | Massimo |
|-----------|---------|
| Violazioni "minori" (Art. 83.4): no DPO, no DPIA, no registro trattamenti | 10M€ o 2% fatturato |
| Violazioni "maggiori" (Art. 83.5): principi base, diritti interessati, trasferimenti extra-UE | **20M€ o 4% fatturato** |

Si applica **il maggiore tra i due**. E in ognuna di queste categorie ci sono violazioni che riguardano direttamente il codice.

---

<a name="cap3"></a>
## Capitolo 3 — NIS 2: chi è "soggetto" e cosa deve fare

> Quanto ci vorrà: 30 minuti.

### 3.1 NIS 2 in 3 righe

**Direttiva NIS 2** = Direttiva (UE) 2022/2555 — Network and Information Security.
Recepita in Italia con il **D.Lgs. 138/2024** (in vigore da ottobre 2024).
Sostituisce la NIS 1 (2016), allargandone enormemente l'ambito.

### 3.2 Chi sono i soggetti NIS 2

Due categorie:

**Soggetti essenziali (Allegato I)** — settori critici:
- Energia (elettricità, gas, petrolio)
- Trasporti (aereo, ferroviario, stradale, navale)
- Banche e mercati finanziari
- Sanità
- Acqua potabile e acque reflue
- Infrastrutture digitali (DNS, TLD, cloud, datacenter)
- Pubbliche amministrazioni centrali e regionali
- Spazio

**Soggetti importanti (Allegato II)**:
- Servizi postali
- Gestione rifiuti
- Manifattura di prodotti critici (chimica, dispositivi medici, ICT)
- Produzione e distribuzione alimentare
- **Servizi digitali** (social network, motori di ricerca, marketplace)
- Ricerca

### 3.3 Soglie dimensionali

NIS 2 si applica a soggetti dei settori sopra **con almeno**:
- 50 dipendenti, OPPURE
- 10M€ di fatturato annuo

Eccezione: alcuni soggetti (es. fornitori di DNS, TLD, telecom) **a prescindere dalle dimensioni**.

### 3.4 Cosa devi fare se sei "soggetto" NIS 2

#### Art. 21 — Misure di gestione dei rischi

Almeno **10 categorie di misure**:

1. Politiche di sicurezza e analisi dei rischi
2. **Gestione degli incidenti**
3. **Continuità operativa** (backup, disaster recovery, gestione crisi)
4. **Sicurezza della supply chain** (rapporti con fornitori)
5. **Sicurezza nell'acquisizione, sviluppo e manutenzione di sistemi**, **gestione delle vulnerabilità**
6. Politiche e procedure di valutazione dell'efficacia
7. **Igiene cibernetica e formazione**
8. Politiche di **cifratura**
9. Sicurezza del personale, controllo accessi, gestione asset
10. **Autenticazione a più fattori**, comunicazioni vocali/video sicure

> Il punto 5 è **direttamente sui processi di sviluppo software**. Ti chiedono di avere SDLC sicuro, gestione vulnerabilità, code review, ecc.

#### Art. 23 — Obbligo di notifica (la differenza con GDPR)

Diversamente dal GDPR (72h), NIS 2 prevede **3 fasi**:

| Tempo | Cosa fai |
|-------|----------|
| **Entro 24 ore** | "Early warning" preliminare al CSIRT/autorità competente |
| **Entro 72 ore** | Notifica completa con dettagli |
| **Entro 30 giorni** | Report finale con cause e misure |

Le 24 ore sono **strette**: serve un piano di incident response.

### 3.5 Sanzioni NIS 2

| Categoria | Massimo |
|-----------|---------|
| Soggetti **essenziali** | 10M€ o 2% fatturato (il maggiore) |
| Soggetti **importanti** | 7M€ o 1,4% fatturato (il maggiore) |

⚠️ **Oltre alla sanzione**: art. 32 prevede la **sospensione temporanea dalla carica** per dirigenti che abbiano commesso violazioni.

### 3.6 GDPR vs NIS 2: quando si applicano insieme?

Spesso. Esempio: una banca italiana ha un breach che espone dati clienti.

- **GDPR** si applica: sono dati personali → notifica al Garante 72h, possibile sanzione fino a 20M€/4%.
- **NIS 2** si applica: la banca è soggetto essenziale → notifica al CSIRT 24h + 72h + 30gg, possibile sanzione fino a 10M€/2%.

Le sanzioni si **cumulano**. E il management può essere sospeso.

---

<a name="cap4"></a>
## Capitolo 4 — Cyber Resilience Act (CRA)

> Quanto ci vorrà: 20 minuti.

### 4.1 CRA in 3 righe

**Cyber Resilience Act** = Regolamento (UE) 2024/2847.
**Entrata in vigore piena: dicembre 2027**.
Si applica a **prodotti con elementi digitali** venduti nel mercato UE.

### 4.2 Cosa cambia con CRA

Per la prima volta in UE, esiste un regolamento che dice: **"un prodotto con software venduto qui deve essere sicuro"**.

Si applica a:
- Prodotti hardware **con software** (router, IoT, dispositivi medici, ecc.)
- **Software puro** (applicazioni, librerie, framework)
- SaaS no (hanno altre normative — NIS 2)

### 4.3 Obblighi principali

I produttori (incluse le software house) devono:

1. **Cybersecurity by design e by default** — analoghi a GDPR Art. 25.
2. **Niente vulnerabilità note** al momento della vendita.
3. **Patching tempestivo** delle vulnerabilità durante il "supporto previsto" (minimo 5 anni di default).
4. **SBOM obbligatorio** — Software Bill of Materials.
5. **Segnalazione attiva di vulnerabilità sfruttate attivamente** entro 24h all'ENISA + autorità nazionale.
6. **Documentazione tecnica** per dimostrare conformità.
7. **Marcatura CE** estesa al cyber.

### 4.4 Categorie di prodotto (criticità diverse)

| Categoria | Esempi | Conformità richiesta |
|-----------|--------|----------------------|
| Default (90% dei prodotti) | App generiche | Auto-valutazione del produttore |
| **Importanti — Classe I** (Allegato III) | Browser, password manager, antivirus, smart home | Auto-valutazione + standard armonizzati |
| **Importanti — Classe II** | Sistemi operativi, hypervisor, firewall, container runtime | Valutazione di terza parte |
| **Critici** (Allegato IV) | Hardware security modules, smart card | Certificazione cyber di terza parte obbligatoria |

### 4.5 Sanzioni CRA

| Violazione | Massimo |
|-----------|---------|
| Non conformità requisiti essenziali | 15M€ o 2,5% fatturato |
| Altre violazioni | 10M€ o 2% fatturato |
| Informazioni false alle autorità | 5M€ o 1% fatturato |

### 4.6 Tempistiche

| Quando | Cosa |
|--------|------|
| Dicembre 2024 | CRA pubblicato |
| Settembre 2026 | Obblighi di notifica vulnerabilità attive |
| **Dicembre 2027** | **Piena applicazione** — niente prodotti non conformi sul mercato UE |

### 4.7 Cosa significa per chi scrive codice

**Tutto cambia per uno sviluppatore di prodotti**:

- Prima del CRA: "spedisco la versione 1.0, se trovo bug li fixo a discrezione".
- Dopo il CRA: "spedisco solo se non ci sono CVE note, devo fixare entro X giorni le CVE che escono per i prossimi 5 anni, tengo SBOM aggiornato".

L'industria si sta preparando ora. Le **prossime CV** in cybersecurity per developer chiederanno familiarità con CRA.

---

<a name="cap5"></a>
## Capitolo 5 — Tabella errore → norma (memorizza questa)

> Questa tabella entra **sempre** nei test del corso.

| Errore tecnico nel codice | Norma | Articolo | Sanzione max |
|---------------------------|-------|----------|--------------|
| **SQL Injection** che espone dati personali | GDPR | Art. 5(1)(f), Art. 32 | 20M€ / 4% |
| **Password salvate in chiaro o con MD5** | GDPR | Art. 32(1)(a) | 20M€ / 4% |
| **No cifratura in transito** (HTTP invece di HTTPS) | GDPR | Art. 32(1)(a) | 20M€ / 4% |
| **Mancata notifica breach entro 72h** | GDPR | Art. 33 | 10M€ / 2% |
| **Form raccoglie dati eccessivi** | GDPR | Art. 5(1)(c) | 20M€ / 4% |
| **Nessuna cancellazione automatica** dopo retention | GDPR | Art. 5(1)(e) | 20M€ / 4% |
| **App di scoring senza intervento umano** (Art. 22) | GDPR | Art. 22, Art. 35 | 20M€ / 4% |
| **No DPIA** per riconoscimento facciale | GDPR | Art. 35 | 10M€ / 2% |
| **Vulnerabilità non gestita** in software CRA | CRA | Art. 11, Art. 13 | 15M€ / 2,5% |
| **No SBOM** in prodotto soggetto CRA | CRA | Art. 13 | 15M€ / 2,5% |
| **Mancata segnalazione 24h** soggetto NIS 2 | NIS 2 | Art. 23 | 10M€ / 2% (ess.) o 7M€ / 1,4% (imp.) |
| **No MFA** in sistema NIS 2 | NIS 2 | Art. 21 | 10M€ / 2% (ess.) o 7M€ / 1,4% (imp.) |
| **No backup** funzionanti in soggetto essenziale | NIS 2 | Art. 21(2)(c) | 10M€ / 2% |
| **No formazione di sicurezza** dei dipendenti | NIS 2 | Art. 21(2)(g) | 10M€ / 2% |
| **Nessuna validazione del fornitore** (supply chain) | NIS 2 | Art. 21(2)(d) | 10M€ / 2% |

> **Lettura veloce**: quasi ogni vulnerabilità che vedremo in M6 è anche una violazione di norma. Saperlo cambia la priorità con cui la affronti.

---

<a name="cap6"></a>
## Capitolo 6 — 5 casi italiani reali

> Provvedimenti del Garante Italiano. Date e cifre verificabili sul sito del Garante (https://www.garanteprivacy.it).

### 6.1 Banca italiana — password in chiaro nel DB (2023)

**Cosa è successo**: una piccola banca italiana subisce un'ispezione del Garante. Esce fuori che il DB clienti aveva password in chiaro (`password = "miopwd123"` direttamente nella tabella users).

**Sanzione**: ~600.000€.

**Articoli**: GDPR Art. 32(1)(a) — sicurezza inadeguata del trattamento.

**Cosa avrebbe dovuto fare lo sviluppatore**: bcrypt o Argon2id (vedi M6.4).

### 6.2 Comune italiano — dati su URL pubblico (2023)

**Cosa è successo**: un comune italiano ha pubblicato online una graduatoria con dati anagrafici, ISEE e altri dati sensibili. URL pubblicamente raggiungibile, indicizzato da Google.

**Sanzione**: ~80.000€.

**Articoli**: GDPR Art. 5(1)(f), Art. 32 — riservatezza non garantita.

**Cosa avrebbe dovuto fare**: pubblicare solo dati anonimizzati o richiedere autenticazione.

### 6.3 Piattaforma e-commerce — IDOR su ordini (2022)

**Cosa è successo**: una piattaforma e-commerce italiana aveva URL `/ordine/<id>` non protetti. Cambiando l'ID si vedevano ordini di altri utenti (con indirizzi, prodotti, importi).

**Sanzione**: ~100.000€.

**Articoli**: GDPR Art. 25, Art. 32.

**Cosa avrebbe dovuto fare**: ownership check server-side (vedi M6.3).

### 6.4 Scuola privata — riconoscimento facciale presenze (2021)

**Cosa è successo**: una scuola privata installa sistema di riconoscimento facciale per registrare presenze, **senza fare DPIA**.

**Sanzione**: ~50.000€ + ordine di rimuovere il sistema.

**Articoli**: GDPR Art. 5, Art. 9, Art. 35.

**Cosa avrebbe dovuto fare**: DPIA + valutazione meno invasiva (badge — vedi V2 esercizio D).

### 6.5 App italiana di delivery — leak token API (2024)

**Cosa è successo**: un'app italiana di delivery espone i propri **token API** in un repository GitHub pubblico. Token con accesso completo al backend, dati clienti, ordini.

**Sanzione**: ~250.000€ + obbligo di notificare gli interessati.

**Articoli**: GDPR Art. 32 — sicurezza del trattamento.

**Cosa avrebbe dovuto fare**: secrets management (HashiCorp Vault, AWS Secrets Manager) + pre-commit hooks per evitare leak su Git.

> **Pattern ricorrente**: in 4 casi su 5, **lo sviluppatore avrebbe potuto evitare** il problema con scelte semplici. La cybersecurity non è "specialità per esperti": è igiene quotidiana.

---

<a name="cap7"></a>
## Capitolo 7 — Diagramma di flusso post-breach

> Cosa fare quando scopri un breach. Stampabile e tienilo vicino.

```
┌──────────────────────────────────────────────────────────────────┐
│                    SCOPERTA DI UN BREACH                          │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
            ┌────────────────────────────────────┐
            │  T+0: STOP. Non chiudere log.       │
            │       Documenta tutto da subito.    │
            │       Avvisa CSO/DPO/management.    │
            └────────────────┬───────────────────┘
                             │
                             ▼
            ┌────────────────────────────────────┐
            │  T+0 a T+1h: Contenimento           │
            │       Isolare il sistema.            │
            │       Bloccare accessi compromessi.  │
            │       Cambiare credenziali.          │
            └────────────────┬───────────────────┘
                             │
                             ▼
            ┌────────────────────────────────────┐
            │  Sei "soggetto" NIS 2?               │
            │       SI ────► Early warning entro 24h│
            │       NO ────► passa al prossimo step │
            └────────────────┬───────────────────┘
                             │
                             ▼
            ┌────────────────────────────────────┐
            │  Ci sono dati personali coinvolti?   │
            │       SI ────► Notifica Garante 72h │
            │       NO ────► passa al prossimo step │
            └────────────────┬───────────────────┘
                             │
                             ▼
            ┌────────────────────────────────────┐
            │  Rischio elevato per gli interessati?│
            │       SI ────► Comunica anche a loro │
            │       NO ────► no comunicazione 1:1 │
            └────────────────┬───────────────────┘
                             │
                             ▼
            ┌────────────────────────────────────┐
            │  T+1 a T+3 giorni: Investigazione   │
            │       Forensics, log analysis.       │
            │       Identificazione cause.         │
            │       Stima danno.                   │
            └────────────────┬───────────────────┘
                             │
                             ▼
            ┌────────────────────────────────────┐
            │  T+ giorni: Remediation             │
            │       Patch, fix codice, rotazione   │
            │       chiavi, rinforzo controlli.    │
            └────────────────┬───────────────────┘
                             │
                             ▼
            ┌────────────────────────────────────┐
            │  T+30 giorni (NIS 2): Report finale │
            │       Cause, impatto, misure.        │
            └────────────────┬───────────────────┘
                             │
                             ▼
            ┌────────────────────────────────────┐
            │  POST-MORTEM                         │
            │       Cosa abbiamo imparato?         │
            │       Aggiornamento threat model     │
            │       (vedi M5).                     │
            └─────────────────────────────────────┘
```

---

<a name="cap8"></a>
## Capitolo 8 — Mini quiz di autovalutazione

> 10 domande veloci. Risposte in fondo.

**Q1.** Entro quante ore devo notificare un breach al Garante?
- a) 24h
- b) 48h
- c) 72h
- d) 7 giorni

**Q2.** Quale articolo del GDPR introduce "Privacy by Design"?
- a) Art. 5
- b) Art. 25
- c) Art. 32
- d) Art. 35

**Q3.** Le sanzioni GDPR massime arrivano a:
- a) 10M€ o 2% fatturato
- b) 20M€ o 4% fatturato
- c) 30M€
- d) Nessun massimo

**Q4.** NIS 2 prevede notifica entro:
- a) Solo 72h
- b) 24h + 72h + 30gg (3 fasi)
- c) Solo 30gg
- d) Solo entro l'anno

**Q5.** Una password salvata in MD5 viola:
- a) GDPR Art. 5(1)(c) — minimizzazione
- b) GDPR Art. 32 — sicurezza del trattamento
- c) Niente, MD5 è ancora ammesso
- d) Solo NIS 2 e solo per soggetti essenziali

**Q6.** CRA si applicherà pienamente da:
- a) Già da 2024
- b) Dicembre 2027
- c) Non è ancora stato approvato
- d) 2030

**Q7.** Una DPIA è obbligatoria per:
- a) Qualunque trattamento
- b) Solo trattamenti con rischio elevato (profilazione, categorie particolari larga scala, sorveglianza)
- c) Solo aziende con >500 dipendenti
- d) Solo se richiesta dal Garante

**Q8.** Un sistema di **riconoscimento facciale per accesso scuola**:
- a) Non richiede DPIA, è una funzionalità di base
- b) Richiede DPIA obbligatoria + alternativa meno invasiva
- c) È vietato per legge sempre
- d) Non è regolato

**Q9.** Una banca italiana subisce un breach con dati personali. Quanti enti deve notificare?
- a) Solo il Garante
- b) Solo CSIRT
- c) Garante (GDPR 72h) + CSIRT/autorità NIS 2 (24h + 72h + 30gg)
- d) Solo gli interessati

**Q10.** SBOM (Software Bill of Materials) sarà obbligatorio per:
- a) Tutti i prodotti UE da subito
- b) Prodotti soggetti a CRA da dicembre 2027
- c) Solo prodotti militari
- d) Mai, è solo una best practice

### Soluzioni

| # | Risp. |
|---|-------|
| Q1 | c — 72h |
| Q2 | b — Art. 25 |
| Q3 | b — 20M€ o 4% |
| Q4 | b — 24h + 72h + 30gg |
| Q5 | b — Art. 32 |
| Q6 | b — Dicembre 2027 |
| Q7 | b — Solo se rischio elevato |
| Q8 | b — DPIA + alternativa |
| Q9 | c — Sia GDPR sia NIS 2 |
| Q10 | b — CRA dal 2027 |

---

## Per approfondire

- **Garante Italiano** — https://www.garanteprivacy.it (provvedimenti, FAQ, linee guida)
- **EDPB (European Data Protection Board)** — https://edpb.europa.eu (linee guida UE)
- **ENISA** — https://www.enisa.europa.eu (NIS 2, CRA, cybersecurity)
- **Testo del GDPR (italiano)**: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **Testo della NIS 2**: https://eur-lex.europa.eu/eli/dir/2022/2555/oj
- **Testo del CRA**: https://eur-lex.europa.eu/eli/reg/2024/2847/oj

---

**Prossimo modulo**: M5 — Security & Privacy by Design (3h). Adesso che sai **cosa la legge richiede**, vediamo come si fa **a progetto**.
