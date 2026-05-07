# Verifica Intermedia 1 — Post M3 (10h)

**Corso:** Cybersecurity e Sicurezza delle Applicazioni — ITS
**Moduli coperti:** M0 + M1 + M2 + M3
**Durata:** 60 minuti
**Punteggio totale:** 100

**Cognome e Nome:** _______________________________
**Data:** _________________________________________

---

## Istruzioni

- 30 domande totali: 20 a scelta multipla (1 punto), 5 a risposta breve (4 punti), 5 esercizi pratici (10 punti). Tot: 100.
- Per le scelta multipla: **1 sola risposta corretta**.
- Per le risposte brevi: **massimo 5 righe**, frasi complete.
- Per gli esercizi: leggi il codice/scenario e rispondi seguendo le indicazioni.

---

## Sezione A — Scelta multipla (20 domande × 1 punto = 20 punti)

**A1.** Cosa significa la "C" della CIA Triad?
- [ ] a) Cryptography
- [ ] b) Confidentiality
- [ ] c) Compliance
- [ ] d) Connectivity

**A2.** Quale di queste **NON** è una proprietà della CIA Triad classica?
- [ ] a) Confidentiality
- [ ] b) Integrity
- [ ] c) Authenticity
- [ ] d) Availability

**A3.** Un attacco DDoS volumetrico viola principalmente:
- [ ] a) Confidentiality
- [ ] b) Integrity
- [ ] c) Availability
- [ ] d) Non-repudiation

**A4.** Quale principio del Secure Coding viene violato quando una webapp gira come root?
- [ ] a) Defense in Depth
- [ ] b) Least Privilege
- [ ] c) Fail Secure
- [ ] d) KISS

**A5.** "Fail Secure" significa:
- [ ] a) Quando il sistema si rompe, lascia passare per non bloccare gli utenti
- [ ] b) Quando il sistema si rompe, cade in uno stato sicuro (default deny)
- [ ] c) Bisogna avere backup giornalieri
- [ ] d) Si deve cifrare tutto

**A6.** Quanti livelli ha il modello ISO/OSI?
- [ ] a) 4
- [ ] b) 5
- [ ] c) 7
- [ ] d) 9

**A7.** A quale livello ISO/OSI lavora TCP?
- [ ] a) Livello 2 (Data Link)
- [ ] b) Livello 3 (Network)
- [ ] c) Livello 4 (Transport)
- [ ] d) Livello 7 (Application)

**A8.** Il MAC address è univoco a quale livello?
- [ ] a) Livello 1 (Fisico)
- [ ] b) Livello 2 (Data Link)
- [ ] c) Livello 3 (Network)
- [ ] d) Livello 4 (Transport)

**A9.** Quale protocollo serve a tradurre un IP in un MAC nella rete locale?
- [ ] a) DNS
- [ ] b) DHCP
- [ ] c) ARP
- [ ] d) ICMP

**A10.** Il three-way handshake TCP è composto da:
- [ ] a) SYN, ACK, FIN
- [ ] b) SYN, SYN-ACK, ACK
- [ ] c) GET, 200 OK, ACK
- [ ] d) Hello, Server Hello, Finished

**A11.** Quale di questi **NON** usa TCP?
- [ ] a) HTTP
- [ ] b) SSH
- [ ] c) DNS (per query brevi)
- [ ] d) FTP

**A12.** ARP spoofing permette principalmente di:
- [ ] a) Bucare il firewall perimetrale
- [ ] b) Eseguire un attacco MITM in rete locale
- [ ] c) Decifrare HTTPS
- [ ] d) Trovare password rubate

**A13.** Quale porta TCP è di default per HTTPS?
- [ ] a) 80
- [ ] b) 443
- [ ] c) 8080
- [ ] d) 53

**A14.** Quale di questi **NON** è un metodo HTTP?
- [ ] a) GET
- [ ] b) POST
- [ ] c) FETCH
- [ ] d) DELETE

**A15.** Lo status code HTTP `403` significa:
- [ ] a) Risorsa non trovata
- [ ] b) Non autenticato
- [ ] c) Autenticato ma non autorizzato
- [ ] d) Errore interno del server

**A16.** Il header `Strict-Transport-Security` (HSTS) serve a:
- [ ] a) Cifrare le password nel DB
- [ ] b) Forzare il browser a usare sempre HTTPS per quel dominio
- [ ] c) Bloccare i cookie di terze parti
- [ ] d) Prevenire SQL injection

**A17.** Il flag `HttpOnly` su un cookie:
- [ ] a) Forza il cookie a viaggiare solo su HTTPS
- [ ] b) Impedisce a JavaScript di leggere quel cookie
- [ ] c) Cifra il cookie
- [ ] d) Rende il cookie permanente

**A18.** Quale stato code HTTP è corretto se l'utente NON è autenticato?
- [ ] a) 400 Bad Request
- [ ] b) 401 Unauthorized
- [ ] c) 403 Forbidden
- [ ] d) 404 Not Found

**A19.** Lo `User-Agent` è:
- [ ] a) Header che identifica il browser/client
- [ ] b) Cookie di sessione
- [ ] c) Indirizzo IP del client
- [ ] d) Nome dell'utente loggato

**A20.** Lo sniffing di rete su Wi-Fi pubblico (caffè, aeroporto) **senza autorizzazione**:
- [ ] a) È legale se è un Wi-Fi gratuito
- [ ] b) È legale per scopi didattici
- [ ] c) È reato in Italia (Art. 617-quater c.p.)
- [ ] d) È legale solo se si è ospiti dell'esercizio

---

## Sezione B — Risposta breve (5 domande × 4 punti = 20 punti)

**B1.** *(4 punti)* Spiega in 3-5 righe la differenza tra **sicurezza informatica** e **sicurezza del software**, facendo un esempio concreto per ognuna.

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

**B2.** *(4 punti)* Cita **3 differenze** tra TCP e UDP. Per ogni differenza, indica un caso d'uso tipico in cui si preferisce uno o l'altro.

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

**B3.** *(4 punti)* Spiega cos'è ARP spoofing, a quale livello OSI lavora, e cita una difesa.

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

**B4.** *(4 punti)* Cosa fanno e come si differenziano gli attributi `Secure`, `HttpOnly` e `SameSite` di un cookie?

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

**B5.** *(4 punti)* Cita **3 dei 5 principi del Secure Coding** e per ognuno fai un esempio concreto di applicazione e uno di violazione.

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

___________________________________________________

---

## Sezione C — Esercizi (5 esercizi × 10 punti = 50 punti)

### C1. Riconoscere il livello OSI *(10 punti)*

Per ognuno dei seguenti **5 termini**, indica a quale livello ISO/OSI appartiene (Livello 1-7). 2 punti per risposta corretta.

| # | Termine | Livello |
|---|---------|---------|
| 1 | Frame Ethernet | _______ |
| 2 | Pacchetto IP | _______ |
| 3 | Segmento TCP | _______ |
| 4 | Cookie HTTP | _______ |
| 5 | Cifratura TLS | _______ |

### C2. Three-way handshake *(10 punti)*

Disegna i 3 messaggi del three-way handshake TCP indicando:
- mittente di ogni messaggio
- nome dei flag TCP impostati a 1
- direzione

```
Client                                   Server
  |                                         |
  |                                         |
  |                                         |
  |                                         |
  |                                         |
```

### C3. Identificare gli header di sicurezza mancanti *(10 punti)*

Dato il seguente output di header HTTP di un sito web:

```
HTTP/1.1 200 OK
Server: nginx/1.18
Content-Type: text/html
Set-Cookie: session=abc123; Path=/
Content-Length: 4521
```

**Quali 4 header di sicurezza sono mancanti?** Per ognuno, spiega in una riga **a cosa serve** e **perché manca è grave**.

| Header mancante | A cosa serve / Perché è grave |
|-----------------|-------------------------------|
| 1. _____________ | _________________________________________________ |
| 2. _____________ | _________________________________________________ |
| 3. _____________ | _________________________________________________ |
| 4. _____________ | _________________________________________________ |

Inoltre, **cosa manca al cookie `session`**? Indica almeno 2 attributi che dovrebbero essere presenti e perché.

___________________________________________________

___________________________________________________

___________________________________________________

### C4. Caso reale — Equifax 2017 *(10 punti)*

L'attacco a Equifax del 2017 (147M di record rubati) è iniziato dallo sfruttamento di una vulnerabilità nota in Apache Struts (CVE-2017-5638), patchata da mesi ma non installata.

Rispondi a queste 4 domande (2.5 punti ciascuna):

1. **Quale proprietà CIA è stata violata?**
   _________________________________________________

2. **A quale categoria di minaccia (tassonomia M1) appartiene?**
   _________________________________________________

3. **Quale dei 5 principi del Secure Coding è stato ignorato?**
   _________________________________________________

4. **Una misura tecnica concreta che avrebbe limitato l'incidente:**
   _________________________________________________

### C5. Mini scenario di rete *(10 punti)*

Apri DevTools del browser e visiti `https://www.example.com`. Vedi una richiesta HTTP che produce questo output (estratto):

```
Request URL: https://www.example.com/api/profilo?id=42
Request Method: GET
Status Code: 200 OK
Set-Cookie: token=eyJhbGciOiJIUzI1NiI...; Path=/

Response body: {
  "id": 42,
  "username": "alice",
  "email": "alice@example.com",
  "balance": 1500.00,
  "ssn": "AAA-BB-CCCC"
}
```

Rispondi (2 punti ciascuna):

1. **Qual è il metodo HTTP usato?** _________________

2. **Cambiando `id=42` in `id=43`, sospetti una vulnerabilità: quale?** _________________________________________________

3. **Quale tipo di dato sensibile non dovrebbe essere nella risposta?** _________________________________________________

4. **Il cookie ha attributi di sicurezza?** Cosa manca? _________________________________________________

5. **Se questo endpoint fosse su HTTP (porta 80) invece che HTTPS, cosa potrebbe vedere un attaccante con Wireshark?** _________________________________________________

---

**FINE — Buon lavoro.**
