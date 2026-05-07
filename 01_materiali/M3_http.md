# Modulo M3 — Protocollo HTTP

**Dispensa Tecnica — Corso ITS Cybersecurity (32h)**
**Modulo 3 — 4 ore (2h teoria + 2h laboratorio)**
**Prerequisiti**: M2 (livelli OSI, TCP/IP, three-way handshake)

> **Materiale di riferimento principale**: `Dispensa_HTTP_ITS_v2_Prodigi.docx` (già didattica, ITS-friendly).
> Questo documento la **integra e la estende** in 4 punti:
> 1. Sicurezza degli header HTTP (approfondimento sostanziale rispetto alla dispensa base)
> 2. Vulnerabilità a livello protocollo (HTTP smuggling, request splitting — cenni)
> 3. Cookie sicuri: `Secure`, `HttpOnly`, `SameSite` con casi pratici
> 4. HTTPS/TLS in profondità (handshake, certificati, errori comuni)

---

## Indice

- [Capitolo 1 — Ripasso veloce HTTP (dalla dispensa base)](#cap1)
- [Capitolo 2 — Header HTTP: la mappa completa](#cap2)
- [Capitolo 3 — Header di sicurezza approfonditi](#cap3)
- [Capitolo 4 — Cookie sicuri: Secure, HttpOnly, SameSite](#cap4)
- [Capitolo 5 — HTTPS e TLS in dettaglio](#cap5)
- [Capitolo 6 — Vulnerabilità a livello protocollo](#cap6)
- [Capitolo 7 — Status code: i casi sottili](#cap7)
- [Capitolo 8 — Lab — Analisi header siti reali](#cap8)
- [Capitolo 9 — Checklist & sintesi](#cap9)

---

<a name="cap1"></a>
## Capitolo 1 — Ripasso veloce HTTP (dalla dispensa base)

> Quanto ci vorrà: 15 minuti.

I capitoli 1-6 della **`Dispensa_HTTP_ITS_v2_Prodigi.docx`** coprono:
- Internet e modello richiesta/risposta
- URL: anatomia (schema, host, porta, path, query, fragment)
- Metodi HTTP (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
- Status code (2xx/3xx/4xx/5xx — overview)
- Headers di base (`Content-Type`, `Authorization`, `Cookie`, `User-Agent`, `Host`)
- Body e JSON

**Vai a leggere quei capitoli prima di proseguire qui** (~30 min). Da questo punto in poi assumiamo che tu sappia:

- Cos'è un GET vs POST.
- Cosa c'è nei `\r\n` separatori header/body.
- Come si legge un URL.
- Cos'è uno status 200, 301, 401, 404, 500.

> Tutto quello che segue **non** è ripetuto nella dispensa base. È contenuto **nuovo** dedicato alla sicurezza.

---

<a name="cap2"></a>
## Capitolo 2 — Header HTTP: la mappa completa

> Quanto ci vorrà: 15 minuti.

Gli header HTTP sono coppie `Nome: valore` che precedono il body. Sono divisi in:

### 2.1 Headers di richiesta (client → server)

| Header | A cosa serve | Esempio |
|--------|--------------|---------|
| `Host` | Dominio richiesto (obbligatorio HTTP/1.1) | `Host: example.com` |
| `User-Agent` | Identifica client/browser | `User-Agent: Mozilla/5.0...` |
| `Accept` | Formati che il client accetta | `Accept: application/json` |
| `Accept-Language` | Lingue preferite | `Accept-Language: it-IT,it;q=0.9` |
| `Authorization` | Credenziali | `Authorization: Bearer eyJhbG...` |
| `Cookie` | Cookie inviati al server | `Cookie: session=abc123` |
| `Content-Type` | Tipo del body inviato | `Content-Type: application/json` |
| `Content-Length` | Lunghezza body in byte | `Content-Length: 47` |
| `Origin` | Origine della richiesta (CORS) | `Origin: https://app.example.com` |
| `Referer` | URL della pagina precedente | `Referer: https://example.com/home` |

### 2.2 Headers di risposta (server → client)

| Header | A cosa serve | Esempio |
|--------|--------------|---------|
| `Content-Type` | Tipo del body restituito | `Content-Type: text/html; charset=utf-8` |
| `Content-Length` | Lunghezza body | `Content-Length: 1043` |
| `Set-Cookie` | Imposta un cookie sul client | `Set-Cookie: session=abc; Secure; HttpOnly` |
| `Location` | URL di redirect (con 3xx) | `Location: /login` |
| `Cache-Control` | Direttive di caching | `Cache-Control: no-store` |
| `Server` | Software server (rivelativo) | `Server: nginx/1.18` |
| `Access-Control-Allow-Origin` | CORS — origini ammesse | `Access-Control-Allow-Origin: https://app.example.com` |

### 2.3 Headers di sicurezza (cuore del modulo)

Sono **specifici di sicurezza**. Una webapp seria li ha quasi tutti. Una webapp scadente non ne ha nessuno. Li vediamo nel cap. 3.

---

<a name="cap3"></a>
## Capitolo 3 — Header di sicurezza approfonditi

> Quanto ci vorrà: 40 minuti. **Cuore del modulo M3 dal punto di vista security**.

Sono il **secondo strumento di difesa più efficace** che hai (dopo "scrivere codice sicuro"). Costano 1 minuto di configurazione, prevengono classi intere di attacchi.

### 3.1 `Strict-Transport-Security` (HSTS)

**A cosa serve**: forza il browser a usare **sempre HTTPS** per quel dominio, anche se l'utente digita `http://`.

**Perché è importante**: difende da **downgrade attacks** e da utenti che digitano `http://` per sbaglio (il primo accesso ancora vulnerabile, ma le visite successive sono protette).

**Sintassi**:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

- `max-age=31536000` → un anno (in secondi)
- `includeSubDomains` → applica anche a `*.example.com`
- `preload` → richiedi inserimento nella **HSTS Preload List** dei browser (così è protetto **anche al primo accesso**)

**Come testare**:
- Visita https://hstspreload.org per vedere se un dominio è in lista.
- DevTools → Network → guarda la response.

**Senza HSTS**: vulnerabile a [SSL Stripping](https://en.wikipedia.org/wiki/SSL_stripping).

### 3.2 `Content-Security-Policy` (CSP)

**A cosa serve**: definisce da quali **origini** il browser può caricare risorse (JS, CSS, immagini, font, ecc.). È la difesa **principale contro XSS** (insieme all'escape dell'output).

**Sintassi base**:
```
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com
```

Significato: caricare solo risorse dal mio stesso dominio, eccezione: gli script possono venire anche da `cdn.example.com`.

**Direttive principali**:

| Direttiva | Cosa controlla |
|-----------|----------------|
| `default-src` | Default per tutto il resto |
| `script-src` | JavaScript |
| `style-src` | CSS |
| `img-src` | Immagini |
| `connect-src` | XHR / fetch / WebSocket |
| `font-src` | Font |
| `frame-ancestors` | Chi può mettere la mia pagina in `<iframe>` |
| `form-action` | Dove i form possono submit-tare |
| `base-uri` | URL base ammesse per `<base>` |

**Sorgenti possibili**:

| Sorgente | Significato |
|----------|-------------|
| `'self'` | Solo dal mio dominio |
| `'none'` | Nessuna fonte (blocca tutto) |
| `https://example.com` | Solo da quell'host |
| `'unsafe-inline'` | Permetti inline script/style ⚠️ |
| `'unsafe-eval'` | Permetti `eval()` ⚠️ |
| `nonce-RANDOM123` | Permetti script con quel nonce |

**Esempio production-grade**:
```
Content-Security-Policy: default-src 'self';
  script-src 'self' 'nonce-r4nd0m';
  style-src 'self';
  img-src 'self' data:;
  connect-src 'self' https://api.example.com;
  font-src 'self';
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
  upgrade-insecure-requests
```

**Come testare**: usa la modalità `Content-Security-Policy-Report-Only` per testare senza bloccare.

### 3.3 `X-Frame-Options`

**A cosa serve**: blocca il **clickjacking** (mettere la tua pagina dentro un iframe per indurre click ingannevoli).

**Valori**:
- `DENY` → mai in iframe.
- `SAMEORIGIN` → solo il mio dominio può fare iframe.
- `ALLOW-FROM uri` → deprecato, non usare.

**Esempio**: `X-Frame-Options: DENY`

> ⚠️ `X-Frame-Options` è ufficialmente deprecato in favore di `Content-Security-Policy: frame-ancestors 'none'`, ma molti browser lo supportano ancora — meglio averli **entrambi**.

### 3.4 `X-Content-Type-Options`

**A cosa serve**: blocca il **MIME sniffing** del browser. Forza il browser a fidarsi del `Content-Type` dichiarato dal server.

**Sintassi (unica)**:
```
X-Content-Type-Options: nosniff
```

**Perché è importante**: senza, un attaccante che riesce a far caricare un file `image.jpg` con dentro JavaScript potrebbe far interpretare quel file come script (se il browser fa MIME sniffing).

### 3.5 `Referrer-Policy`

**A cosa serve**: controlla quali informazioni vengono nel header `Referer` quando l'utente clicca un link verso un altro dominio.

**Valori più usati**:
- `no-referrer` → mai inviare Referer.
- `strict-origin` → invia solo l'origine (es. `https://example.com`, non l'URL completo).
- `strict-origin-when-cross-origin` → URL completo intra-site, solo origin cross-site. **Default moderno.**
- `same-origin` → invia solo se same-origin.

**Esempio sicuro**: `Referrer-Policy: strict-origin-when-cross-origin`

**Perché conta**: senza, se sulla tua pagina c'è un link a un servizio terzo, gli mandi l'URL completo della tua pagina (incluso eventuali parametri sensibili nella query string).

### 3.6 `Permissions-Policy` (ex Feature-Policy)

**A cosa serve**: controlla quali **API del browser** la tua pagina (e i suoi iframe) possono usare.

**Sintassi**:
```
Permissions-Policy: camera=(), microphone=(), geolocation=(self), payment=()
```

Significato:
- camera → vietata a tutti
- microphone → vietato a tutti
- geolocation → solo same-origin
- payment → vietato a tutti

**Lista API**: camera, microphone, geolocation, payment, usb, accelerometer, gyroscope, magnetometer, fullscreen, autoplay, encrypted-media, picture-in-picture, ecc.

**Perché serve**: previene che codice JS o iframe non fidato attivi feature invasive.

### 3.7 `Cross-Origin-*-Policy` (avanzato, cenno)

Tre header moderni:
- `Cross-Origin-Opener-Policy: same-origin` (COOP) — isola la finestra da altri origin
- `Cross-Origin-Embedder-Policy: require-corp` (COEP) — costringe risorse a dichiarare CORS
- `Cross-Origin-Resource-Policy: same-origin` (CORP) — controlla chi può caricare la mia risorsa

Insieme abilitano features come `SharedArrayBuffer` e proteggono da Spectre-style attacks. Se non ti servono, ignorali. Se ti servono, studia bene l'effetto a cascata.

### 3.8 `Server` (rimuovere o falsificare)

Non è un header di sicurezza positivo: è uno **da nascondere**.

Default di nginx: `Server: nginx/1.18.0`. Questo dice all'attaccante:
- Sto usando nginx 1.18.0 → cerca CVE specifiche di quella versione.

**Migliore pratica**: rimuovere o oscurare:
- nginx: `server_tokens off;` in config.
- Apache: `ServerTokens Prod`, `ServerSignature Off`.
- Flask in produzione: usare un reverse proxy che rimuova il `Server` di Werkzeug.

### 3.9 Tabella riassuntiva

| Header | Difende da | Esempio sicuro |
|--------|-----------|-----------------|
| `Strict-Transport-Security` | Downgrade HTTP | `max-age=31536000; includeSubDomains; preload` |
| `Content-Security-Policy` | XSS, data injection | `default-src 'self'` (poi raffina) |
| `X-Frame-Options` | Clickjacking | `DENY` |
| `X-Content-Type-Options` | MIME sniffing | `nosniff` |
| `Referrer-Policy` | Info leak via Referer | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | API browser invasive | `camera=(), microphone=()` |
| `Server` (rimuovere) | Fingerprinting | (vuoto o falso) |

> **Test rapido del tuo sito**: https://securityheaders.com — assegna un voto da F a A+.
> Anche siti famosi prendono spesso B o C. È quasi mai A+.

---

<a name="cap4"></a>
## Capitolo 4 — Cookie sicuri: Secure, HttpOnly, SameSite

> Quanto ci vorrà: 25 minuti.

I cookie sono il **modo principale per tenere lo stato della sessione** in HTTP. Se sono compromessi, l'attaccante "diventa" l'utente.

### 4.1 Cookie senza protezione: il caso peggiore

```
Set-Cookie: session=abc123; Path=/
```

Cosa manca a questo cookie:
- ❌ Va anche su HTTP (sniffabile).
- ❌ JavaScript può leggerlo (`document.cookie`) → XSS lo ruba.
- ❌ Va in richieste cross-site → CSRF.

### 4.2 `Secure`

```
Set-Cookie: session=abc123; Secure
```

Il browser invia il cookie **solo su HTTPS**. Se lo invii su HTTP, il browser lo scarta.

**Quando usarlo**: sempre, su qualunque cookie di sessione/autenticazione.

**Errore comune**: fare sviluppo locale su HTTP e dimenticarsi `Secure` in produzione. Soluzione: configurazione per ambiente.

### 4.3 `HttpOnly`

```
Set-Cookie: session=abc123; HttpOnly
```

JavaScript **non può leggere** questo cookie. `document.cookie` non lo restituisce.

**Quando usarlo**: sempre, su cookie di sessione/auth. Così uno **XSS non può rubare il token**.

**Eccezione**: se hai bisogno che JS legga il cookie (es. per inviarlo come header in API), **non puoi usare HttpOnly**. In tal caso, il pattern moderno è:
- Cookie HttpOnly per la sessione.
- Token CSRF separato (anti-CSRF), questo sì leggibile da JS.

### 4.4 `SameSite`

L'header più importante per CSRF. 3 valori possibili:

#### `SameSite=Strict`

Il cookie viene inviato **solo** se la richiesta parte dallo stesso sito.

Esempio: l'utente clicca un link da `evil.com` verso `bank.com/transfer`. Il browser **non** invia il cookie di `bank.com`. CSRF mitigato.

⚠️ **Effetto collaterale**: anche un link legittimo da Google a `bank.com` non porta il cookie. L'utente sembrerà non loggato all'arrivo. Per molti casi è troppo restrittivo.

#### `SameSite=Lax` (default moderno dei browser)

Il cookie è inviato in **navigazione top-level** (click su link, bookmark) ma non in richieste cross-site automatiche (form auto-submit, immagini).

È un buon compromesso: difende da CSRF nelle situazioni più pericolose, mantiene UX normale.

#### `SameSite=None`

Sempre inviato (anche cross-site). **Richiede obbligatoriamente `Secure`**.

Da usare solo per cookie che **devono** essere disponibili cross-site (es. SSO).

### 4.5 Esempio completo "best practice"

```
Set-Cookie: session=abc123;
            Secure;
            HttpOnly;
            SameSite=Lax;
            Path=/;
            Max-Age=3600
```

In **Flask**, configurazione corrispondente:

```python
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=3600,
)
```

### 4.6 Cookie prefixes (avanzato)

Due prefissi speciali rendono i cookie **inviolabili**:

- `__Secure-` → il cookie deve avere `Secure` e essere stato impostato da HTTPS. Esempio: `Set-Cookie: __Secure-session=abc; Secure`.
- `__Host-` → deve avere `Secure`, `Path=/`, no `Domain`, e essere stato impostato da HTTPS. Massima sicurezza per cookie di host.

Esempio: `Set-Cookie: __Host-session=abc; Secure; Path=/; HttpOnly; SameSite=Strict`.

---

<a name="cap5"></a>
## Capitolo 5 — HTTPS e TLS in dettaglio

> Quanto ci vorrà: 25 minuti.

In M2 abbiamo detto "HTTPS = HTTP cifrato con TLS". Adesso vediamo come funziona davvero.

### 5.1 Cosa fa TLS (in 3 punti)

1. **Cifratura**: i messaggi sono illeggibili a chi sniffa.
2. **Autenticazione**: il client verifica che il server sia chi dice di essere (via certificato).
3. **Integrità**: i messaggi non possono essere modificati senza che il client se ne accorga.

### 5.2 Versioni TLS

| Versione | Stato | Note |
|----------|-------|------|
| SSL 1, 2, 3 | ❌ MORTO | Vulnerabilità note (POODLE, BEAST), non usare mai |
| TLS 1.0 | ❌ MORTO | Deprecato dal 2020 |
| TLS 1.1 | ❌ MORTO | Deprecato dal 2020 |
| TLS 1.2 | ✅ OK | Standard de facto, ancora largamente usato |
| TLS 1.3 | ✅ MEGLIO | RFC 8446 (2018). Più veloce, più sicuro |

**In produzione moderna**: TLS 1.2 minimo, TLS 1.3 preferito.

### 5.3 Il TLS handshake (versione semplificata 1.2)

```
Client                                   Server
  │                                          │
  │  ─ Client Hello ───►                     │  (versione TLS, cipher suites supportate, random_C)
  │                                          │
  │  ◄─ Server Hello ─                       │  (cipher suite scelta, random_S)
  │  ◄─ Certificate ─                        │  (certificato del server)
  │  ◄─ Server Key Exchange ─                │  (parametri scambio chiavi DH)
  │  ◄─ Server Hello Done ─                  │
  │                                          │
  │  ─ Client Key Exchange ───►              │  (parametri DH del client)
  │  ─ Change Cipher Spec ───►               │
  │  ─ Finished (cifrato) ───►               │
  │                                          │
  │  ◄─ Change Cipher Spec ─                 │
  │  ◄─ Finished (cifrato) ─                 │
  │                                          │
  │  ═══════════ CANALE CIFRATO ═══════════  │
  │  (HTTP cifrato con la chiave di sessione) │
```

In TLS 1.3 questo handshake è **più corto** (1-RTT, una sola coppia di scambi prima di poter inviare dati).

### 5.4 I certificati

Il certificato del server è firmato da una **Certificate Authority** (CA) di cui il browser si fida.

**Cosa contiene**:
- Nome di dominio (es. `*.example.com`).
- Chiave pubblica del server.
- Validità (data inizio + scadenza).
- Firma della CA emittente.
- Catena: server cert → intermediate cert → root cert.

**Il browser verifica** in ordine:
1. Il dominio coincide con il `Host` richiesto?
2. Il certificato è valido (non scaduto, non revocato)?
3. La firma porta a una CA root presente nel mio "trust store"?

Se uno di questi salta → warning di sicurezza (e talvolta blocco completo).

### 5.5 Errori TLS comuni in classe

| Sintomo | Causa | Soluzione |
|---------|-------|-----------|
| "Your connection is not private" — `NET::ERR_CERT_AUTHORITY_INVALID` | Certificato self-signed o CA non fidata | Reinstalla certificato valido (Let's Encrypt è gratuito) |
| "Certificate has expired" | Certificato scaduto | Rinnovare. Use **certbot** per Let's Encrypt: rinnovo automatico |
| "Certificate name mismatch" | Cert per `www.example.com` ma vai su `example.com` | Includere entrambi nel SAN |
| "Mixed content" | Pagina HTTPS che carica risorse HTTP | Migrare tutto a HTTPS, usare `upgrade-insecure-requests` in CSP |

### 5.6 Lab di scoperta: SSL Labs

Vai a https://www.ssllabs.com/ssltest/

Inserisci un dominio. Il tool ti dà un voto da A+ a F valutando:
- Supporto cipher suites
- Versioni TLS attive
- Vulnerabilità note (Heartbleed, BEAST, POODLE)
- Configurazione certificato
- HSTS

Sito serio = A o A+. Sito scadente = B o peggio.

> **Esercizio in classe**: il docente fa testare 3 siti scelti dalla classe. Confronto.

### 5.7 Il problema del certificato self-signed in dev

In sviluppo locale spesso uno usa certificati self-signed. Il browser dà warning. Il discente impara a "cliccare sempre Avanzato → Procedi".

⚠️ **Pessima abitudine**. Quando trovi un warning **in produzione**, devi prenderlo sul serio.

**Best practice in dev**:
- Usa `mkcert` (https://github.com/FiloSottile/mkcert) per generare certificati locali firmati da una CA che il tuo browser riconosce. Niente più warning.
- Oppure usa Let's Encrypt anche per ambienti di sviluppo accessibili online.

---

<a name="cap6"></a>
## Capitolo 6 — Vulnerabilità a livello protocollo (cenni)

> Quanto ci vorrà: 10 minuti. Solo overview, queste sono materia avanzata.

### 6.1 HTTP Request Smuggling

L'attaccante invia una richiesta strutturata in modo che frontend (es. CDN/load balancer) e backend la interpretino diversamente. Risultato: una "seconda richiesta nascosta" finisce dentro il flusso del prossimo utente.

**Impatto**: bypass autenticazione, cache poisoning, hijacking sessioni.

**Difese**: server moderni con parsing strict, configurazione di front/back coerente, niente HTTP/1.0 in catena.

### 6.2 HTTP Response Splitting

L'attaccante inietta `\r\n` in un parametro che finisce in un header (es. `Location` di redirect). Il `\r\n` chiude l'header e ne inietta uno nuovo.

**Impatto**: cache poisoning, XSS via header injection.

**Difese**: validazione/sanitizzazione di tutti gli input che finiscono in header. Le librerie moderne (Flask, Express, ASP.NET) bloccano `\r\n` di default — il bug nasce quando si bypassano queste protezioni.

### 6.3 Slowloris (DoS applicativo)

L'attaccante apre molte connessioni HTTP **lentissime** che non chiude mai. Il server riserva risorse (thread, FD) e si esaurisce.

**Difese**: timeout aggressivi (es. nginx `client_header_timeout 10s`), reverse proxy davanti all'app, rate limit per IP.

### 6.4 HTTP/2 e HTTP/3 (cenni)

- **HTTP/2** (RFC 7540, 2015): multiplexing, header compression (HPACK), server push. Più veloce ma con vulnerabilità specifiche (HTTP/2 rapid reset CVE-2023-44487).
- **HTTP/3** (QUIC): trasporto su UDP, riduce latenza. In produzione su Google, Cloudflare. Vulnerabilità ancora in fase di scoperta.

> Per il corso ITS basta sapere che **esistono**. Le difese applicative (header, cookie, codice sicuro) **valgono uguale** per tutte le versioni.

---

<a name="cap7"></a>
## Capitolo 7 — Status code: i casi sottili

> Quanto ci vorrà: 15 minuti.

La dispensa base copre i 2xx/3xx/4xx/5xx classici. Qui i casi che fanno errori in produzione e che entrano nei test.

### 7.1 401 vs 403 (la confusione storica)

| Code | Nome | Quando usarlo |
|------|------|---------------|
| 401 | Unauthorized | **Non autenticato**. Manca il login. (Nome storico fuorviante: dovrebbe essere "Unauthenticated".) |
| 403 | Forbidden | **Autenticato, ma non ha i permessi**. (Es. user normale prova a accedere a `/admin`.) |

**Errore comune**: webapp che restituisce 401 sempre, anche per errori di autorizzazione. Confonde il client e i tool di monitoring.

### 7.2 404 vs 410

| Code | Nome | Quando usarlo |
|------|------|---------------|
| 404 | Not Found | "Non lo trovo, magari non è mai esistito o l'URL è sbagliato." |
| 410 | Gone | "Esisteva, ma è stato rimosso permanentemente, non tornerà." |

**Quando usare 410**: quando hai cancellato volontariamente una risorsa e vuoi che i motori di ricerca la rimuovano dall'indice prima.

### 7.3 422 Unprocessable Entity

Status spesso ignorato. Significa: "ho capito la richiesta sintatticamente, ma semanticamente è sbagliata".

**Esempio**: POST `/users` con `{"email": "non-email", "age": -5}`. Sintatticamente è JSON valido (no 400), ma i valori non hanno senso (no 200). Risposta giusta: **422**.

### 7.4 429 Too Many Requests

Per **rate limiting**. Dovresti combinare con header `Retry-After: 60` (secondi prima del prossimo tentativo permesso).

```
HTTP/1.1 429 Too Many Requests
Retry-After: 60
Content-Type: application/json

{"error": "rate limit exceeded"}
```

### 7.5 451 Unavailable for Legal Reasons

(Numero ispirato a Fahrenheit 451 di Ray Bradbury.) Indica che la risorsa è bloccata per motivi legali (es. ordine giudiziario di rimozione).

### 7.6 5xx — quale serve davvero?

| Code | Quando |
|------|--------|
| 500 Internal Server Error | Errore generico. **Default** per eccezioni non gestite. **Non rivelare lo stack trace.** |
| 502 Bad Gateway | Reverse proxy non riceve risposta valida dal backend. |
| 503 Service Unavailable | Servizio temporaneamente non disponibile (deploy, sovraccarico). Combinare con `Retry-After`. |
| 504 Gateway Timeout | Reverse proxy timeout sul backend. |

**Errore catastrofico**: rispondere 500 con `{"error": "...", "stack_trace": "..."}` in produzione. Information disclosure (vedi STRIDE in M5).

---

<a name="cap8"></a>
## Capitolo 8 — Lab — Analisi header siti reali (40 min totali)

### 8.1 Lab M3.1 — DevTools Discovery (30 min)

> Coperto dal **syllabus M3** e dalla dispensa HTTP base. Riassunto:

1. Apri DevTools (F12) → Network.
2. Apri 3 siti: `https://github.com`, `https://www.google.com`, un sito di un servizio italiano (es. INPS, banca).
3. Per ognuno, identifica e annota:
   - Numero di richieste totali.
   - Status code della richiesta principale.
   - 3 header di risposta scelti.
   - Cookie ricevuti (vedi tab Application → Cookies).

### 8.2 Lab M3.2 — Header analysis con `requests` (10 min)

Già preparato in `02_lab/M3.2_http_client.py`. Eseguilo, poi rispondi:

1. Quanti dei **6 header di sicurezza principali** sono presenti su `https://github.com`?
2. E su `https://www.python.org`?
3. E su un sito di tua scelta?
4. Quale è quasi sempre presente? Quale è quasi sempre mancante?

Tipico risultato:
- `Strict-Transport-Security`: presente ovunque.
- `X-Content-Type-Options`: presente quasi ovunque.
- `Content-Security-Policy`: spesso assente o molto debole.
- `Permissions-Policy`: raro.

### 8.3 Bonus — Confronto con securityheaders.com

Vai a https://securityheaders.com → testa 3 siti.

Confronta il voto del sito (A+ a F) con il numero di header che hai trovato col tuo script.

---

<a name="cap9"></a>
## Capitolo 9 — Checklist & sintesi

### 9.1 Checklist HTTP per la tua webapp

```
☐ TLS 1.2+ (ideale 1.3) attivo, TLS <1.2 disabilitato
☐ Certificato valido (non self-signed, non scaduto)
☐ Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
☐ Content-Security-Policy: default-src 'self' (o più stringente)
☐ X-Frame-Options: DENY
☐ X-Content-Type-Options: nosniff
☐ Referrer-Policy: strict-origin-when-cross-origin
☐ Permissions-Policy: minimal allow-list
☐ Cookie sessione: Secure; HttpOnly; SameSite=Lax (o Strict)
☐ Cookie auth con __Host- prefix (massima sicurezza)
☐ Server: header rimosso o oscurato
☐ Error handler: 500 generico, no stack trace in produzione
☐ Rate limiting: 429 con Retry-After
☐ Status code corretti (401 vs 403, 404 vs 410)
☐ Nessuna info sensibile nella query string (GET)
☐ HTTPS-only redirect 301 da http://
```

### 9.2 Antipattern da evitare

- ❌ "Tanto ho HTTPS, non mi servono gli header di sicurezza."
- ❌ "Il certificato self-signed va bene per ora, lo cambieremo." (No, lo dimenticherai.)
- ❌ Cookie senza `HttpOnly` → XSS = furto sessione.
- ❌ Cookie senza `SameSite` → CSRF.
- ❌ 500 con stack trace al client.
- ❌ 200 OK con `{"success": false}` nel body. Status code mente, parsing complicato.
- ❌ Password nella query string GET.

### 9.3 Errori da evitare in classe

- **Non saltare HSTS** quando spieghi HTTPS — è un concetto chiave per chi non l'ha mai sentito.
- **Non fare il discorso TLS handshake all'inizio**. Falli prima toccare `requests` e DevTools, poi spiegherai cosa c'è "sotto".
- **Non liquidare `SameSite=Lax/Strict` in 30 secondi**. È uno degli aspetti meno conosciuti e più importanti per CSRF — vale 10 minuti pieni.

### 9.4 Per approfondire

- **MDN Web Docs** — riferimento per ogni header HTTP.
- **OWASP Secure Headers Project**: https://owasp.org/www-project-secure-headers/
- **Mozilla Observatory**: https://observatory.mozilla.org — analizza i tuoi header, ti dà raccomandazioni.
- **Bjornson, Ben (LogRocket)** — articoli pratici su CSP.

---

**Prossimo modulo**: M4 — Quadro Normativo (2h). Adesso che sai cosa fare tecnicamente, vediamo cosa la legge richiede.
