# Modulo M2 — Networking & ISO/OSI

**Dispensa Tecnica — Corso ITS Cybersecurity (32h)**
**Modulo 2 — 6 ore (3h teoria + 3h laboratorio)**
**Prerequisiti**: nessuno. Si parte da "cos'è una rete".

---

## Indice

- [Capitolo 1 — Cos'è una rete (l'analogia postale)](#cap1)
- [Capitolo 2 — I due modelli: ISO/OSI vs TCP/IP](#cap2)
- [Capitolo 3 — Livello 1 e 2: Fisico e Data Link](#cap3)
- [Capitolo 4 — ARP: dal IP al MAC](#cap4)
- [Capitolo 5 — Livello 3: Network (IP, ICMP, routing)](#cap5)
- [Capitolo 6 — Livello 4: Transport (TCP, UDP, porte)](#cap6)
- [Capitolo 7 — Livelli 5-7: Sessione, Presentazione, Applicazione](#cap7)
- [Capitolo 8 — La sicurezza in rete è "a strati"](#cap8)
- [Capitolo 9 — Lab Wireshark](#cap9)
- [Capitolo 10 — Lab Python: socket, port scanner, scapy](#cap10)
- [Capitolo 11 — Sintesi e checklist finale](#cap11)

---

<a name="cap1"></a>
## Capitolo 1 — Cos'è una rete (l'analogia postale)

> Quanto ci vorrà: 20 minuti.
> Cosa devi sapere prima: nulla.

Prima di parlare di protocolli, indirizzi, porte e attacchi, dobbiamo capire una cosa: **cos'è una rete?**

Una rete è un insieme di dispositivi che si scambiano informazioni. Stop. Non c'è altro. Tutto il resto è dettaglio implementativo.

Però "scambiarsi informazioni" è una frase generica. Per fare le cose serie, dobbiamo affrontare problemi pratici:

- Come fanno due computer a sapere "dove si trova" l'altro?
- Come fanno a parlarsi se sono in continenti diversi?
- Come fanno a non confondere il messaggio uno con quello dell'altro?
- Cosa succede se un messaggio si perde lungo la strada?
- Come fanno a parlarsi in modo sicuro se chiunque può ascoltare?

Tutte queste domande sono già state risolte. Le soluzioni si chiamano **protocolli**. Un protocollo è un accordo: "se tu fai così, io faccio cosà". Quando due computer comunicano, lo fanno seguendo un mucchio di protocolli sovrapposti, ognuno responsabile di un pezzo del problema.

### L'analogia postale (la useremo per tutto il modulo)

Immagina di voler spedire una lettera dalla tua casa a Milano a un amico a New York.

Tu ti occupi solo di:

- Scrivere il **contenuto** della lettera.
- Mettere la lettera in una **busta**.
- Scrivere **mittente** (tuo) e **destinatario** (suo) sulla busta.
- Mettere il **francobollo**.
- Mettere la busta nella **buca delle lettere**.

Da quel momento, non ti interessa più cosa succede. Eppure dietro le quinte succede di tutto:

- Le Poste **smistano** la tua lettera (Italia → Stati Uniti).
- La caricano su un **camion** (poi un aereo, poi un altro camion).
- A New York un **postino** la consegna al palazzo.
- La porta nella **cassetta** di tuo amico.

Questo è esattamente come funziona una rete. Tu (l'app) scrivi il messaggio. Sotto di te ci sono **livelli** di servizi, ognuno con un compito specifico, che si occupano di farlo arrivare. Il livello "applicazione" non sa niente di camion. Il livello "trasporto" non sa niente del contenuto della tua lettera. Ognuno fa il suo pezzo.

Questo principio si chiama **stratificazione**. È il concetto più importante di questo modulo. Tieniti stretta l'analogia postale: la useremo a ogni livello.

---

<a name="cap2"></a>
## Capitolo 2 — I due modelli: ISO/OSI vs TCP/IP

> Quanto ci vorrà: 30 minuti.

Esistono due modelli per organizzare i livelli di rete. Uno è **teorico**, l'altro è **pratico**. Vedremo entrambi, ma poi useremo soprattutto il secondo.

### 2.1 Il modello ISO/OSI (teorico, 7 livelli)

ISO/OSI è stato pubblicato nel 1984 dall'ISO (International Organization for Standardization). È un modello di **riferimento**: dice come *dovrebbe* essere fatta una rete in modo pulito.

| Livello | Nome | Cosa fa | Esempi di protocolli |
|---------|------|---------|---------------------|
| 7 | Application | Interfaccia con l'utente/app | HTTP, FTP, SMTP, DNS |
| 6 | Presentation | Formattazione dati (JSON, XML, cifratura) | TLS/SSL, ASCII, JPEG |
| 5 | Session | Gestione sessioni | NetBIOS, RPC |
| 4 | Transport | Trasporto end-to-end (affidabilità, ordine) | TCP, UDP |
| 3 | Network | Indirizzamento, routing tra reti | IP, ICMP, ARP, OSPF |
| 2 | Data Link | Trasmissione tra nodi adiacenti, MAC | Ethernet, Wi-Fi (802.11) |
| 1 | Physical | Bit elettrici, ottici, radio | Cavi, fibre, segnali |

**Mnemonica per memorizzare** (dal basso): "**P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way" (Physical, Data link, Network, Transport, Session, Presentation, Application).

### 2.2 Il modello TCP/IP (pratico, 4 livelli)

TCP/IP è il modello che usa Internet **realmente**. È più semplice: 4 livelli invece di 7. I livelli 5-6-7 di OSI sono accorpati in un unico "Application".

| Livello TCP/IP | Mappa OSI | Cosa fa | Protocolli |
|----------------|-----------|---------|-----------|
| 4. Application | OSI 5+6+7 | Tutto quello che fa l'app | HTTP, DNS, TLS, SMTP, FTP |
| 3. Transport | OSI 4 | TCP, UDP | TCP, UDP |
| 2. Internet | OSI 3 | IP, routing | IP, ICMP, ARP* |
| 1. Network Access | OSI 1+2 | Ethernet, Wi-Fi | Ethernet, 802.11 |

*ARP è formalmente al livello 2/3, dipende dalla fonte.

### 2.3 Perché studiamo ISO/OSI se nessuno lo usa?

Buona domanda. Risposta:

1. **È più chiaro per imparare**: 7 livelli ben separati ti aiutano a capire chi fa cosa.
2. **È il vocabolario standard**: quando un collega dice "il problema è a livello 4", parla in termini OSI.
3. **Aiuta a ragionare sulla sicurezza**: ogni livello ha vulnerabilità tipiche. Vederle stratificate è didatticamente utile.

Nel resto del modulo useremo OSI come *mappa concettuale* e TCP/IP come *implementazione reale*.

### 2.4 Il viaggio di una richiesta HTTP attraverso i livelli

Quando il tuo browser richiede `https://example.com`, succede questo:

```
[Browser]                            <- Livello 7 (Application): genera richiesta HTTP
    ↓
[TLS]                                <- Livello 6 (Presentation): cifra
    ↓
[TCP segment]                        <- Livello 4 (Transport): porta destinazione 443, sequenza
    ↓
[IP packet]                          <- Livello 3 (Network): indirizzo IP destinazione
    ↓
[Ethernet frame]                     <- Livello 2 (Data Link): MAC del prossimo hop (router)
    ↓
[bit elettrici/ottici]               <- Livello 1 (Physical): bit sul cavo / Wi-Fi
```

Ogni livello aggiunge un **header** ai dati che riceve dal livello sopra. È come mettere busta dentro busta dentro busta. Quando arriva al destinatario, ogni livello apre la sua busta e passa il contenuto al livello successivo.

Questo si chiama **incapsulamento**.

---

<a name="cap3"></a>
## Capitolo 3 — Livello 1 e 2: Fisico e Data Link

> Quanto ci vorrà: 25 minuti.

### 3.1 Livello 1 — Fisico

Si occupa di trasmettere **bit** (0 e 1) attraverso un mezzo fisico:

- **Cavi in rame** (UTP/STP per Ethernet)
- **Fibra ottica** (per backbone, dorsali, GbE+)
- **Onde radio** (Wi-Fi 2.4/5/6 GHz, Bluetooth)
- **Onde luminose** (li-fi, raro)

Non parla di "indirizzi" o "messaggi". Parla solo di "questo segnale ha questo voltaggio per X microsecondi → è un 1".

**Vulnerabilità tipiche del livello 1**:
- **Wiretapping**: intercettazione fisica del cavo (sniffing passivo).
- **Jamming**: disturbare un segnale Wi-Fi con un trasmettitore sulla stessa frequenza (DoS fisico).
- **Eavesdropping Wi-Fi**: chiunque nelle vicinanze può catturare frame Wi-Fi (poi serve la chiave per decifrarli).

### 3.2 Livello 2 — Data Link

Si occupa di trasmettere **frame** (gruppi di bit con un inizio e una fine) tra due dispositivi **direttamente connessi**.

Concetti chiave:

- **MAC address**: l'identificativo univoco di una scheda di rete (NIC). 48 bit, scritti in esadecimale, es: `00:1A:2B:3C:4D:5E`. È *fisicamente* impresso nella scheda dal produttore.
- **Frame Ethernet**: la "busta" di livello 2. Contiene MAC mittente, MAC destinatario, tipo di payload, payload, checksum.
- **Switch**: dispositivo che inoltra frame in base al MAC destinatario. Più "intelligente" di un hub.

```
+----------------------------------------------------+
| Frame Ethernet                                     |
+--------+--------+--------+----------+--------+----+
| Pream- | MAC    | MAC    | Type/Len | Payload | FCS |
| ble    | dst    | src    | (16 bit) | (≤1500B)| (CRC)|
| (8 B)  | (6 B)  | (6 B)  |          |         | (4B)|
+--------+--------+--------+----------+----------+----+
```

**Vulnerabilità tipiche del livello 2**:

- **MAC spoofing**: l'attaccante cambia il proprio MAC per impersonare un altro dispositivo (banalissimo: `ifconfig` su Linux, o software gratuiti su Windows).
- **MAC flooding**: si bombarda lo switch con frame da tanti MAC diversi finché la sua tabella CAM si riempie. Quando la CAM è piena, lo switch si comporta come un hub e **trasmette tutto a tutti** → possibile sniffing.
- **VLAN hopping**: tecniche per "saltare" da una VLAN all'altra (double tagging, switch spoofing).

> **Difese L2**: port security sugli switch (limita MAC per porta), DHCP snooping, dynamic ARP inspection, VLAN segregation, 802.1X (autenticazione di porta).

---

<a name="cap4"></a>
## Capitolo 4 — ARP: dal IP al MAC

> Quanto ci vorrà: 20 minuti.

### 4.1 Il problema

Tu hai l'**IP** del destinatario (es. `192.168.1.10`). Ma per spedire il frame Ethernet serve il **MAC**. Come si fa a trovarlo?

Risposta: **ARP — Address Resolution Protocol**.

### 4.2 Come funziona ARP

```
[Computer A]                              [Computer B]
192.168.1.5                               192.168.1.10
00:11:22:33:44:55                         AA:BB:CC:DD:EE:FF

Step 1: A vuole parlare con B (192.168.1.10) ma non sa il suo MAC.

Step 2: A manda una ARP request in BROADCAST a tutta la rete:
"Chi ha l'IP 192.168.1.10? Risponda al MAC 00:11:22:33:44:55."

Step 3: Tutti ricevono. Solo B risponde:
"L'IP 192.168.1.10 è mio, e il mio MAC è AA:BB:CC:DD:EE:FF."

Step 4: A salva la coppia (192.168.1.10 → AA:BB:CC:DD:EE:FF) nella sua
        ARP cache, e ora può spedire frame Ethernet diretti a B.
```

Provalo tu: apri il terminale e digita `arp -a` (Windows/Linux/macOS). Vedrai la tua ARP cache.

### 4.3 La vulnerabilità: ARP Spoofing (a.k.a. ARP Poisoning)

Il protocollo ARP **non ha autenticazione**. Chiunque può rispondere "sì sono io" e i computer ci credono.

**Scenario di attacco**:

1. Tu (vittima) e l'attaccante siete sulla stessa rete locale (es. caffè con Wi-Fi).
2. L'attaccante manda continuamente frame ARP **non richiesti** dicendo "l'IP del gateway è il mio MAC".
3. Tu li credi (nessuna verifica) e aggiorni la cache: pensi che il gateway sia l'attaccante.
4. Da ora tutto il traffico che mandi al gateway passa **prima** dall'attaccante.
5. Lui può: leggerlo (sniffing), modificarlo (MITM), o bloccarlo (DoS).

Questo si chiama **Man-in-the-Middle (MITM)** ed è la base di moltissimi attacchi di rete. Tool storico: `ettercap`, `bettercap`.

> **Difesa**: ARP statici per host critici (gateway), Dynamic ARP Inspection (DAI) sugli switch enterprise, monitoraggio ARP cache, **HTTPS** ovunque (se tutto è cifrato, l'MITM vede solo dati cifrati).

---

<a name="cap5"></a>
## Capitolo 5 — Livello 3: Network (IP, ICMP, routing)

> Quanto ci vorrà: 30 minuti.

### 5.1 Cos'è IP

Ethernet funziona solo dentro una LAN (rete locale). Per parlare con un computer **dall'altra parte del mondo**, serve un sistema di indirizzamento globale e un meccanismo di **routing** (instradamento).

**IP — Internet Protocol** è esattamente questo. Il "P" delle Poste della nostra analogia.

Esistono due versioni:

- **IPv4**: 32 bit, ~4 miliardi di indirizzi, scritti come `192.168.1.10`. È quello che usiamo nel 90% dei casi.
- **IPv6**: 128 bit, indirizzi enormi tipo `2001:0db8:85a3::7334`. Pensato per quando IPv4 finirà (lo è quasi).

### 5.2 Indirizzi privati e pubblici

Non tutti gli IP sono "su Internet". Alcuni range sono **privati** (riservati per reti interne):

- `10.0.0.0/8` (10.x.x.x)
- `172.16.0.0/12` (172.16.x.x – 172.31.x.x)
- `192.168.0.0/16` (192.168.x.x — il classico)

Dentro casa tua, il router ti dà un IP privato (es. `192.168.1.10`). Per andare su Internet, fa **NAT** (Network Address Translation): traduce il tuo IP privato nel suo IP pubblico, e ricorda chi ha richiesto cosa.

### 5.3 ICMP

ICMP è il protocollo "diagnostico" del livello 3. Lo usano comandi come:

- `ping`: invia pacchetti ICMP Echo Request, aspetta Echo Reply. Se arrivano, l'host è raggiungibile.
- `traceroute` (Linux/macOS) / `tracert` (Windows): scopre il percorso che prendono i pacchetti per arrivare a destinazione.

**Vulnerabilità tipiche del livello 3**:

- **IP spoofing**: l'attaccante mette nel campo "mittente" un IP che non è il suo. Funziona perché IP non ha autenticazione. Usato in attacchi DDoS amplificati e in alcuni MITM.
- **ICMP flood / Ping of Death**: bombardare un host con ping fino a metterlo KO (oggi raro grazie a rate limiting).
- **Smurf attack**: mandi un ping con IP mittente spoofato (quello della vittima) all'indirizzo broadcast. Tutti rispondono alla vittima, sommergendola.
- **IP fragmentation attacks** (Tear Drop): pacchetti IP frammentati malformati che crashano i sistemi vecchi.

> **Difese L3**: firewall (filtraggio per IP/porta), reverse path filtering (anti-spoofing), rate limiting ICMP, segregazione di rete, VPN, **non esporre nulla che non deve esserlo**.

### 5.4 Subnetting (cenno)

Una rete IP si divide in sottoreti per organizzare il traffico. La maschera di rete (es. `255.255.255.0` o `/24`) dice "questi 24 bit identificano la sottorete, gli altri 8 identificano l'host".

Esempio: `192.168.1.0/24` → 256 indirizzi (da `.0` a `.255`), di cui `.0` è la rete e `.255` è il broadcast. Restano 254 host utilizzabili.

> Il subnetting è importante per chi fa l'amministratore di rete. In questo corso ci basta sapere che esiste e che separa il traffico per sicurezza/efficienza. Per approfondire: dispensa OSPF.

### 5.5 Routing (cenno)

Quando un IP non è "vicino" (stessa LAN), il pacchetto va al **gateway** (di solito il router di casa/ufficio). Il gateway lo passa al suo gateway, e così via, finché arriva. Ogni passaggio si chiama **hop**.

I router decidono dove inoltrare i pacchetti consultando una **tabella di routing**, popolata da:

- Configurazione manuale (rotte statiche)
- Protocolli dinamici (OSPF, BGP, RIP)

Per le vulnerabilità di routing dinamico (es. BGP hijacking), si rimanda a un corso di networking avanzato.

---

<a name="cap6"></a>
## Capitolo 6 — Livello 4: Transport (TCP, UDP, porte)

> Quanto ci vorrà: 30 minuti. **È il livello più importante per noi**.

### 6.1 Il problema che il livello 4 risolve

Hai un IP (sai dov'è il computer) ma:

- Quale **applicazione** dentro quel computer deve ricevere il dato? (Su un PC c'è il browser, l'email, Skype, il giocone… tutti ascoltano la rete.)
- Il dato arriva **integro**? **In ordine**? Se manca un pezzo, lo richiediamo?
- Possiamo aprire più "conversazioni" parallele?

Per questi problemi servono le **porte** e i protocolli di trasporto **TCP** e **UDP**.

### 6.2 Le porte

Una porta è un numero da 0 a 65535. Ogni "conversazione" usa una coppia di porte (sorgente e destinazione).

Le porte si dividono in:

- **Well-known ports** (0–1023): assegnate dalla IANA a servizi standard. Esempi:
  - 22 — SSH
  - 23 — Telnet (legacy, insicuro)
  - 25 — SMTP
  - 53 — DNS
  - 80 — HTTP
  - 443 — HTTPS
  - 3389 — RDP
- **Registered ports** (1024–49151): assegnabili a software registrati. Es: 3306 (MySQL), 5432 (PostgreSQL), 27017 (MongoDB), 8080 (HTTP alternativo).
- **Dynamic/private** (49152–65535): usate dai client per le proprie connessioni temporanee.

**Concetto chiave**: un client che apre una connessione verso un server non sa la propria porta a priori. Il sistema operativo gliene assegna una libera (effemera). Quindi `tu (192.168.1.5:54321) → server (93.184.216.34:443)`.

### 6.3 TCP — Connection-oriented, affidabile

TCP (Transmission Control Protocol) garantisce:

- **Affidabilità**: se un pacchetto si perde, viene rispedito.
- **Ordine**: i pacchetti vengono ricomposti nell'ordine giusto anche se arrivano disordinati.
- **Flow control**: il mittente non saturа il destinatario.
- **Connection-oriented**: serve un "saluto" iniziale (handshake) prima di trasmettere.

#### Il three-way handshake

Quando apri una connessione TCP, succede questo:

```
Client                                          Server
  │                                               │
  │ ─── SYN (vuoi iniziare?) ──→                  │
  │                                               │
  │                  ←── SYN-ACK (sì, anche tu?) ─│
  │                                               │
  │ ─── ACK (sì, partiamo!) ──→                   │
  │                                               │
  │  ═══ Connessione stabilita, scambio dati ═══  │
  │                                               │
```

Tre messaggi, e la connessione è pronta. Da qui si possono scambiare i dati veri (es. HTTP).

Quando finisci, c'è un equivalente "FIN handshake" per chiudere pulitamente.

#### Vulnerabilità tipiche di TCP

- **Port scanning**: l'attaccante manda SYN a molte porte. Se riceve SYN-ACK, la porta è aperta; se riceve RST, è chiusa. Tool: `nmap`. Il port scanning **non è di per sé un attacco**, ma è la base della ricognizione di un attaccante.
- **SYN flood**: l'attaccante manda migliaia di SYN senza completare l'handshake. Il server riserva risorse per ognuno e finisce la memoria → DoS. Difesa: SYN cookies, rate limiting, firewall stateful.
- **TCP hijacking**: se l'attaccante può vedere il traffico (MITM) e indovinare il sequence number TCP, può inserirsi nella connessione. Oggi raro grazie a sequence number randomizzati e HTTPS.
- **TCP reset attacks**: forgiare pacchetti RST per chiudere connessioni altrui (richiede MITM o conoscenza dei seq).

### 6.4 UDP — Connectionless, veloce

UDP (User Datagram Protocol) è il "no-frills":

- **Niente handshake**: spedisci, e via.
- **Niente garanzia di consegna**: se il pacchetto si perde, pazienza.
- **Niente ordine**: arrivano come capita.
- **Niente flow control**: bombardi quanto vuoi.

Sembra inutile, ma è perfetto quando:

- Velocità > affidabilità: streaming video/audio, giochi online, VoIP.
- Messaggi piccoli e singoli: DNS query, ARP, NTP.
- Multicast (un solo invio a molti destinatari).

#### Vulnerabilità tipiche di UDP

- **UDP flood**: facile fare DoS (nessun handshake = nessun rate limit naturale).
- **DNS amplification**: l'attaccante manda piccole DNS query con IP mittente spoofato (la vittima). Il server DNS risponde con grandi pacchetti **alla vittima**, amplificando il traffico 50-100x.
- **NTP amplification**: stesso pattern con NTP (server di tempo).

### 6.5 Tabella riassuntiva TCP vs UDP

| Caratteristica | TCP | UDP |
|----------------|-----|-----|
| Connessione | Sì (handshake) | No |
| Affidabilità | Sì | No |
| Ordine | Sì | No |
| Velocità | Più lento | Più veloce |
| Overhead | 20 byte header | 8 byte header |
| Tipici utenti | HTTP, HTTPS, SSH, FTP, email | DNS, VoIP, giochi, video streaming |

---

<a name="cap7"></a>
## Capitolo 7 — Livelli 5-7: Sessione, Presentazione, Applicazione

> Quanto ci vorrà: 15 minuti.

I livelli sopra il trasporto sono dove vivono le **applicazioni**. Per ognuno una riga:

- **Livello 5 (Session)**: stabilisce, mantiene, chiude le sessioni. Esempio: SSL/TLS handshake è qui (spesso considerato a cavallo 5/6).
- **Livello 6 (Presentation)**: codifica/decodifica dei dati. Cifratura (TLS), compressione, conversione di charset (ASCII ↔ UTF-8).
- **Livello 7 (Application)**: il protocollo che vedi tu come utente o sviluppatore. **HTTP**, FTP, SMTP, DNS, SSH, IMAP/POP3, ecc.

Studieremo HTTP a fondo nel **modulo M3**. Qui ci interessa vedere le **vulnerabilità tipiche** di questi livelli.

### 7.1 DNS — Domain Name System (UDP/53, TCP/53 per zone transfer)

Traduce nomi (`example.com`) in IP (`93.184.216.34`).

**Vulnerabilità DNS**:

- **DNS spoofing / cache poisoning**: l'attaccante inietta risposte false nella cache DNS di un server, dirottando utenti su siti malevoli. (CVE storiche: Kaminsky 2008.)
- **DNS hijacking**: prendere il controllo del DNS dell'utente (modificando il router casalingo, malware, MITM).
- **DNS tunneling**: nascondere comunicazioni dentro query DNS legittime (canale C2 furtivo per malware).

> **Difesa**: DNSSEC (firma le risposte DNS), DoT/DoH (DNS over TLS/HTTPS — cifra le query DNS), DNS server affidabili.

### 7.2 TLS/SSL — Transport Layer Security

Cifra il livello applicativo. È quello che mette la "S" in HTTPS.

**Vulnerabilità storiche**:

- **Heartbleed (CVE-2014-0160)**: bug in OpenSSL che permetteva di leggere memoria del server (chiavi private, password, ecc.). Catastrofico.
- **POODLE, BEAST, CRIME, BREACH**: attacchi a varianti vecchie di SSL/TLS.
- **Downgrade attacks**: forzare il client a usare una versione TLS debole. **Difesa: HSTS** (vedremo in M3).
- **Self-signed o expired certificates**: se il client li accetta senza warning → MITM possibile.

> **Difesa**: TLS 1.2+ ovunque, certificati validi, HSTS, certificate pinning per app mobile, test SSL Labs.

### 7.3 HTTP (overview, dettagli in M3)

HTTP **in chiaro** è leggibile da chiunque sniffi. Headers, cookie, password, dati sensibili: tutto visibile.

> **Difesa**: HTTPS ovunque. Non c'è un "ma non è importante che sia cifrato". Lo è sempre.

---

<a name="cap8"></a>
## Capitolo 8 — La sicurezza in rete è "a strati"

> Quanto ci vorrà: 10 minuti. Questo è il messaggio chiave del modulo.

Ogni livello ha vulnerabilità tipiche. Ogni livello ha difese tipiche. **La sicurezza non è di un livello solo**: è la somma delle difese di tutti.

### Tabella delle difese per livello

| Livello | Vulnerabilità tipica | Difesa primaria |
|---------|----------------------|-----------------|
| 7 — Application | XSS, SQLi, IDOR, CSRF | Codice sicuro (M6 del corso) |
| 6 — Presentation | TLS downgrade, cipher deboli | TLS 1.2+, HSTS |
| 5 — Session | Session hijacking | Cookie sicuri, token rotation |
| 4 — Transport | SYN flood, port scan | Firewall stateful, rate limiting |
| 3 — Network | IP spoofing, ICMP flood | Reverse path filtering, ACL |
| 2 — Data Link | ARP spoofing, MAC flooding | Port security, DAI, 802.1X |
| 1 — Physical | Wiretapping, jamming | Sicurezza fisica, cifratura |

### Un esempio concreto: come si difende un'app web seria

Pensa a una banca online. Le difese stratificate:

- **Fisico**: data center con accesso controllato, ridondanza linee.
- **Data Link**: switch enterprise con port security, VLAN segregate.
- **Network**: firewall perimetrale, IPS, segmentazione DMZ.
- **Transport**: rate limiting, anti-DDoS.
- **Session/TLS**: TLS 1.3, HSTS, certificate transparency.
- **Application**: WAF (Web Application Firewall), input validation, query parametrizzate.
- **Sopra a tutto**: monitoraggio, logging, incident response.

Se ne togli **una sola**, l'attaccante prende quella strada. Defense in Depth ricorda?

---

<a name="cap9"></a>
## Capitolo 9 — Lab Wireshark

> Quanto ci vorrà: 45 minuti.

### 9.1 Cos'è Wireshark

Wireshark è il **gold standard** per analizzare traffico di rete. Cattura i pacchetti che passano dalla tua scheda di rete, li scompone livello per livello, e te li mostra leggibili.

Non è un attacco: è uno strumento di **diagnosi**. Ma può essere usato anche da chi vuole sniffare la rete altrui — quindi:

> ⚠️ **REGOLA D'ORO**:
> Si fa Wireshark **solo sulla propria macchina** o su **reti di laboratorio**.
> Mai su reti pubbliche (caffè, aeroporto), aziendali, scolastiche **senza autorizzazione esplicita**. Sarebbe **reato** (Art. 617-quater c.p. — "Intercettazione, impedimento o interruzione illecita di comunicazioni informatiche").

### 9.2 Installazione

**Windows/macOS**: scarica da [wireshark.org](https://www.wireshark.org). L'installer include Npcap (driver per la cattura), accetta tutti i default.

**Linux Ubuntu/Debian**:
```bash
sudo apt install wireshark
sudo usermod -aG wireshark $USER  # per non dover usare sudo
# logout e re-login
```

### 9.3 Lab M2.1 — Wireshark Discovery (45 min)

**Obiettivo**: catturare il traffico di una visita a un sito HTTP e a uno HTTPS, e identificare i livelli OSI in azione.

**Setup**:
1. Apri Wireshark.
2. Seleziona la tua interfaccia di rete (di solito "Wi-Fi" o "Ethernet").
3. Click "Start" (icona pinna blu).
4. Apri il browser.

#### Step 1 — Cattura HTTP in chiaro (10 min)

Apri `http://example.com` (NON HTTPS, è una pagina che funziona ancora in chiaro per i lab). Aspetta 5 secondi e ferma la cattura (icona quadrato rosso).

Nel filtro Wireshark in alto, scrivi `http` e premi Invio.

Cosa devi trovare:
- Una richiesta `GET / HTTP/1.1` (espandi il pacchetto, vedrai gli header)
- La risposta `HTTP/1.1 200 OK` con il contenuto HTML

**Espansione pacchetto**: clicca su una riga, sotto vedrai i livelli:
```
Frame 12: 845 bytes captured                    ← Livello 1 (Physical/Frame)
Ethernet II, Src: ..., Dst: ...                  ← Livello 2 (Data Link)
Internet Protocol Version 4, Src: ..., Dst: ...  ← Livello 3 (Network)
Transmission Control Protocol, Src: 54322, Dst: 80 ← Livello 4 (Transport)
Hypertext Transfer Protocol                       ← Livello 7 (Application)
```

**Domanda di verifica**: che IP ha `example.com`? In che porta? Quale livello te lo dice?

#### Step 2 — Cattura HTTPS (10 min)

Stessa cosa con `https://example.com`. Nel filtro: `tls`.

Cosa cambia:
- Vedi un **TLS handshake** (Client Hello, Server Hello, Certificate, Key Exchange).
- Dopo l'handshake, **non vedi più HTTP**: vedi solo "Application Data" cifrato. Buono.

**Domanda**: confronta i due capture. Cosa è leggibile in HTTP che non è leggibile in HTTPS?

#### Step 3 — Three-Way Handshake (15 min)

Filtra `tcp.flags.syn == 1`. Trova:

1. Un **SYN** dal tuo IP al server (porta destinazione 80 o 443).
2. Un **SYN-ACK** dal server al tuo IP.
3. Un **ACK** dal tuo IP al server.

Questi tre pacchetti sono il three-way handshake! Annotali, fai screenshot.

#### Step 4 — DNS Query (10 min)

Filtra `dns`. Trova la query `example.com` e la sua risposta. Quale IP è stato restituito? (Controlla con `nslookup example.com` da terminale.)

### 9.4 Output del lab

Salva il file `.pcapng` come `M2_1_lab_capture.pcapng`. Scrivi un breve documento (1 pagina) con:

- IP e porta del server `example.com`.
- 1 screenshot del three-way handshake.
- Differenza HTTP vs HTTPS.
- IP restituito dalla risposta DNS.

---

<a name="cap10"></a>
## Capitolo 10 — Lab Python: socket, port scanner, scapy

> Quanto ci vorrà: ~80 minuti per i 3 lab.

### Lab M2.2 — Client TCP con socket (30 min)

**Obiettivo**: scrivere a mano una richiesta HTTP usando solo i socket TCP del livello 4. Confrontare con Wireshark.

```python
# 02_lab/M2.2_socket_tcp.py
import socket

HOST = "example.com"
PORT = 80

# Step 1: crea socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 2: connetti (questo è il three-way handshake!)
s.connect((HOST, PORT))
print(f"[+] Connesso a {HOST}:{PORT}")

# Step 3: invia richiesta HTTP a mano
request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Connection: close\r\n"
    "\r\n"
)
s.sendall(request.encode())

# Step 4: leggi la risposta
response = b""
while True:
    chunk = s.recv(4096)
    if not chunk:
        break
    response += chunk

print(response.decode("utf-8", errors="replace"))
s.close()
```

**Esegui**: `python M2.2_socket_tcp.py`. Vedrai gli header HTTP e il body HTML.

**Wireshark in parallelo**: cattura prima di lanciare lo script, ferma dopo. Trova il tuo three-way handshake, la GET, la risposta. È **lo stesso** della pagina aperta dal browser, solo che qui l'hai scritta tu.

**Domanda di approfondimento**: cosa cambia se rimuovi `Connection: close`? Perché?

### Lab M2.3 — Mini Port Scanner (30 min)

**Obiettivo**: scrivere un port scanner basico, capire il principio.

```python
# 02_lab/M2.3_port_scanner.py
import socket
from concurrent.futures import ThreadPoolExecutor

TARGET = "127.0.0.1"            # SOLO localhost o macchine di lab
PORTS_TO_SCAN = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445,
                 3306, 5432, 5900, 8080, 8443]
TIMEOUT = 1.0

def scan_port(port: int) -> tuple[int, bool]:
    """Restituisce (porta, aperta?)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    try:
        s.connect((TARGET, port))
        return (port, True)
    except (socket.timeout, ConnectionRefusedError, OSError):
        return (port, False)
    finally:
        s.close()

print(f"[*] Scansione di {TARGET}...\n")

with ThreadPoolExecutor(max_workers=20) as ex:
    results = list(ex.map(scan_port, PORTS_TO_SCAN))

for port, is_open in results:
    status = "APERTA" if is_open else "chiusa"
    print(f"  Porta {port:5d} : {status}")
```

**Esegui**: `python M2.3_port_scanner.py`.

**Esercizi**:
1. Modifica per scansionare un range continuo: `range(1, 1024)`.
2. Aggiungi banner grabbing: dopo la connect, manda `b"\r\n"` e leggi la risposta. Su porta 22 vedrai `SSH-2.0-OpenSSH_X.Y` → questo è **fingerprinting**, base del pentesting.
3. Confronta il tuo output con `nmap -sT 127.0.0.1`.

> ⚠️ **Avvertenza legale ribadita**: scansionare host che **non sono tuoi** (o di cui non hai autorizzazione scritta) è reato (Art. 615-ter c.p.). Usa `127.0.0.1` o macchine virtuali del corso. Mai IP pubblici a caso.

### Lab M2.4 — Scapy Sniffer (20 min)

**Obiettivo**: catturare pacchetti dalla propria interfaccia in Python (mini-Wireshark).

**Installazione**: `pip install scapy`

**Permessi**: devi lanciare lo script con privilegi elevati (Windows: PowerShell come Amministratore; Linux/macOS: `sudo`).

```python
# 02_lab/M2.4_scapy_sniff.py
from scapy.all import sniff, IP, TCP, UDP

def process(pkt):
    if IP in pkt:
        proto = "TCP" if TCP in pkt else "UDP" if UDP in pkt else "OTHER"
        src = pkt[IP].src
        dst = pkt[IP].dst
        sport = pkt.sport if (TCP in pkt or UDP in pkt) else "-"
        dport = pkt.dport if (TCP in pkt or UDP in pkt) else "-"
        print(f"[{proto}] {src}:{sport} -> {dst}:{dport}")

print("[*] Cattura 30 pacchetti...")
sniff(prn=process, count=30, store=False)
print("[+] Fine.")
```

**Esegui**: `sudo python M2.4_scapy_sniff.py` (Linux/macOS) o PowerShell admin (Windows).

Mentre gira, apri un browser e visita un sito qualsiasi. Vedrai pacchetti TCP verso la porta 443 del server.

**Esercizio**: aggiungi un filtro BPF per catturare solo il traffico HTTPS:
```python
sniff(prn=process, count=30, store=False, filter="tcp port 443")
```

---

<a name="cap11"></a>
## Capitolo 11 — Sintesi e checklist finale

### 11.1 Cosa devi sapere alla fine di M2

- ✅ Disegnare la pila ISO/OSI a 7 livelli e mappare TCP/IP a 4.
- ✅ Per ogni livello: cosa fa, almeno un protocollo, almeno una vulnerabilità.
- ✅ Spiegare ARP e ARP spoofing.
- ✅ Spiegare il three-way handshake TCP.
- ✅ Differenza TCP vs UDP e quando si usa cosa.
- ✅ Aprire Wireshark, catturare traffico, leggere i livelli.
- ✅ Scrivere un client socket TCP minimal in Python.
- ✅ Scrivere un port scanner basico in Python.
- ✅ Sapere che lo sniffing/scanning su reti non proprie è **reato**.

### 11.2 Errori tipici da evitare

- ❌ Pensare che HTTPS "rende sicura" l'app. HTTPS protegge il **canale**, non l'app. SQL Injection passa lo stesso.
- ❌ Confondere MAC e IP. Il MAC è L2 (fisso, locale), l'IP è L3 (cambia con la rete).
- ❌ Pensare che il firewall sia l'unica difesa. È **una delle** difese.
- ❌ Lanciare nmap su IP pubblici per "vedere come va". Reato in Italia.

### 11.3 Per approfondire

- **Networking serio**: dispensa OSPF (in `Dispense varie`).
- **Wireshark**: PortSwigger Web Academy ha lab gratuiti.
- **Sicurezza di rete**: TryHackMe "Network Fundamentals" (gratuito).
- **Pentest in modo legale**: HackTheBox starting point, OverTheWire Bandit.

---

**Prossimo modulo**: M3 — Protocollo HTTP (4h). Ora che sai come arrivano i bit fino al livello 7, vediamo cosa c'è davvero dentro una richiesta HTTP.
