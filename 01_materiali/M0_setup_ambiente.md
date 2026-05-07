# Modulo M0 — Setup ambiente di lavoro

**Dispensa Tecnica — Corso ITS Cybersecurity (32h)**
**Modulo 0 — 2 ore (0,5h teoria + 1,5h laboratorio)**
**Prerequisiti**: nessuno. Si parte dal computer appena acceso.

> Questo modulo **non parla di sicurezza**. Parla di come **predisporre l'ambiente** che useremo per imparare la sicurezza nei prossimi 30 ore.
>
> Salta questo passaggio e troverai tutti gli altri capitoli incomprensibili: i comandi non funzioneranno, gli esempi non gireranno, e penserai che il problema sia il tuo. Non lo sarà — sarà l'ambiente.

> **Materiale di riferimento principale**: Capitolo 0 della dispensa `dispensa-sviluppo-sicuro-software.docx`. Questo materiale è una versione **operativa per le 2 ore in aula**, con focus su:
> - Cosa va fatto in classe vs in autonomia
> - Verifiche di completamento per ogni step
> - Troubleshooting dei problemi più comuni in aula

---

## Indice

- [Capitolo 1 — Cosa installeremo (e perché)](#cap1)
- [Capitolo 2 — In aula (90 min): le 4 installazioni guidate](#cap2)
- [Capitolo 3 — A casa (compito tra G1 e G2)](#cap3)
- [Capitolo 4 — Troubleshooting per il docente](#cap4)
- [Capitolo 5 — Verifica di completamento](#cap5)
- [Capitolo 6 — Routine quotidiana del corso](#cap6)

---

<a name="cap1"></a>
## Capitolo 1 — Cosa installeremo (e perché)

Per tutto il corso ci serviranno **5 strumenti**. Te li elenco subito così sai dove stiamo andando:

| # | Strumento | A cosa serve | Quando |
|---|-----------|--------------|--------|
| 1 | **Python 3.12+** | Linguaggio di tutti i lab | M0 (in aula) |
| 2 | **Visual Studio Code** | Editor di testo "intelligente" | M0 (in aula) |
| 3 | **Git** | Scaricare BancaPiccola | M0 (a casa) |
| 4 | **DB Browser for SQLite** | Sbirciare dentro i database | M0 (a casa) |
| 5 | **Browser moderno** (Chrome/Edge/Firefox) | Lab HTTP, DevTools | già installato |
| 6 | **Wireshark** | Analisi traffico di rete | M2 (lo aggiungiamo poi) |
| 7 | **curl** | Test HTTP da terminale | M3 (incluso in Windows 10+) |

**Tutto gratuito, tutto multipiattaforma**. Nessun costo, nessun account a pagamento.

### Perché Python e non Java/JavaScript/C#?

Per 3 motivi:

1. **Sintassi pulita**: chi non ha mai programmato impara più velocemente con Python.
2. **Ecosistema cybersecurity**: Python è il linguaggio standard di scripting per security (scapy, requests, beautifulsoup, sqlmap, ecc.).
3. **Flask**: framework web minimal, perfetto per costruire BancaPiccola passo-passo.

Quello che imparerai vale per **qualsiasi linguaggio** — i concetti di SQL injection, XSS, IDOR sono universali. Python è solo lo strumento.

---

<a name="cap2"></a>
## Capitolo 2 — In aula (90 min): le 4 installazioni guidate

### 2.1 Installa Python 3.12 (15 min)

**Su Windows**:

1. Apri il browser → vai a [python.org/downloads](https://www.python.org/downloads/)
2. Click sul pulsante giallo **"Download Python 3.12.x"**
3. Apri il file scaricato (`python-3.12.x-amd64.exe`)
4. ⚠️ **CRUCIALE**: nella prima schermata dell'installer, **spunta "Add python.exe to PATH"** (in basso). Senza questo, niente funziona dopo.
5. Click "Install Now"
6. Aspetta che finisca, click "Close"

**Su macOS**:
- Stessa procedura da python.org, oppure `brew install python@3.12` se hai Homebrew.

**Su Linux (Ubuntu/Debian)**:
```bash
sudo apt update && sudo apt install python3.12 python3.12-venv python3-pip
```

### 2.2 Verifica che funzioni

Apri **un nuovo** terminale (importante: deve essere nuovo, dopo l'installazione):

- **Windows**: cerca "PowerShell" nel menu Start
- **macOS**: cerca "Terminal" in Spotlight
- **Linux**: già lo conosci

Digita:

```
python --version
```

Output atteso (la versione esatta può variare):
```
Python 3.12.7
```

> **Se non funziona**: vedi cap 4 troubleshooting.

### 2.3 Installa Visual Studio Code (15 min)

1. Vai a [code.visualstudio.com](https://code.visualstudio.com)
2. Scarica la versione per il tuo OS
3. Installalo con i default (su Windows, lascia tutte le checkbox spuntate)
4. Apri VS Code

**Estensioni essenziali** (pannello sinistra → icona "Extensions"):

- **Python** (di Microsoft): aggiunge supporto completo a Python.
- **Pylance** (di Microsoft): si installa in automatico con Python, analisi statica.

> ⚠️ Salta tutte le altre estensioni. Le aggiungeremo solo se servono. KISS.

### 2.4 Il terminale: cos'è, come si apre (10 min)

Il **terminale** è una finestra dove scrivi comandi al computer in formato testuale. È più veloce e potente del cliccare con il mouse — e in cybersecurity lo usi continuamente.

**Comandi base che useremo sempre**:

| Windows PowerShell | macOS/Linux | Cosa fa |
|--------------------|--------------|---------|
| `cd C:\miacartella` | `cd /home/me/miacartella` | Cambia cartella |
| `cd ..` | `cd ..` | Sale di un livello |
| `dir` | `ls` | Lista i file |
| `mkdir nome` | `mkdir nome` | Crea cartella |
| `python file.py` | `python3 file.py` | Esegue uno script Python |
| `pip install pkg` | `pip3 install pkg` | Installa una libreria Python |

**Esercizio cronometrato (3 min)**: ognuno apre il terminale, naviga sul Desktop con `cd`, crea una cartella `cybersec-its` con `mkdir`, ci entra dentro con `cd cybersec-its`. Chi finisce alza la mano.

### 2.5 La tua prima cartella di lavoro + Hello World (15 min)

Da dentro `cybersec-its/` (controlla con `pwd` su macOS/Linux o `Get-Location` su Windows):

**1. Crea il file** `hello.py` con VS Code:

```
code hello.py
```

(Se `code` non funziona da terminale, apri VS Code → File → Open Folder → cybersec-its.)

**2. Scrivi questo nel file**:

```python
print("Ciao! Sono pronto per il corso ITS di cybersecurity.")
```

**3. Salva** (`Ctrl+S` / `Cmd+S`).

**4. Esegui** dal terminale:

```
python hello.py
```

Output atteso:
```
Ciao! Sono pronto per il corso ITS di cybersecurity.
```

✅ Se vedi questo messaggio, **sei pronto al 50%**.

### 2.6 Ambienti virtuali (15 min)

Un **ambiente virtuale** (`venv`) è una cartella isolata che contiene una copia di Python e le sue librerie, **separata dal sistema**. Serve per non sporcare il Python globale e per avere progetti indipendenti.

> Pensa a un venv come al tuo "studio di lavoro": dentro tieni i tuoi attrezzi senza mescolarli con quelli degli altri progetti.

**Creazione**: dalla cartella `cybersec-its`:

```
python -m venv .venv
```

Si crea una cartella `.venv/`.

**Attivazione** (qui le sintassi divergono):

| OS | Comando |
|----|---------|
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows CMD | `.venv\Scripts\activate.bat` |
| macOS/Linux | `source .venv/bin/activate` |

⚠️ **Errore PowerShell comune**: "running scripts is disabled". Soluzione una volta sola:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Poi riprova.

**Verifica attivazione**: nel prompt deve apparire `(.venv)` all'inizio:
```
(.venv) PS C:\Users\tu\cybersec-its>
```

✅ Se lo vedi, l'ambiente è attivo. **Da qui in avanti tutto il `pip install` e `python` userà questa cartella isolata**.

### 2.7 Flask: la tua prima pagina web (15 min)

Con `(.venv)` attivo:

```
pip install flask
```

(Vedi scaricare e installare Flask + dipendenze. Dura ~30 secondi.)

Crea il file `hello_flask.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Ciao, sono BancaPiccola in mini.</h1>"

if __name__ == "__main__":
    app.run(debug=True)
```

Esegui:

```
python hello_flask.py
```

Output atteso (estratto):
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
 * Restarting with stat
```

**Apri il browser** → vai a [http://127.0.0.1:5000](http://127.0.0.1:5000)

✅ Vedi "Ciao, sono BancaPiccola in mini." → **sei pronto al 100% per la parte in aula**.

Per fermare il server: `Ctrl+C` nel terminale.

---

<a name="cap3"></a>
## Capitolo 3 — A casa (compito tra G1 e G2)

Le installazioni di **Git** e **DB Browser for SQLite**, e il **clone di BancaPiccola**, si fanno in autonomia tra il primo e il secondo incontro. Sono semplici (~30 minuti totali) ma vanno fatte tutte.

### 3.1 Git

1. Scarica da [git-scm.com](https://git-scm.com/downloads)
2. Su Windows: lascia tutti i default tranne "Default editor used by Git" → seleziona **Visual Studio Code**.
3. Su macOS: `brew install git` o l'installer ufficiale.
4. Linux: `sudo apt install git`.

**Verifica**: `git --version` deve restituire una versione (es. `git version 2.43.0`).

### 3.2 DB Browser for SQLite

1. Scarica da [sqlitebrowser.org](https://sqlitebrowser.org/dl/)
2. Installa con i default.
3. Verifica aprendolo: deve aprirsi una finestra con tre pannelli.

### 3.3 Clone di BancaPiccola

Da terminale, **dentro `cybersec-its`**:

```
git clone https://github.com/PROFILO/BancaPiccola.git
```

> Il link esatto te lo fornisce il docente — è il repo del corso.

Verifica:
```
cd BancaPiccola
ls
```

Devi vedere `BancaPiccola-vuln/` e `BancaPiccola-secure/`.

### 3.4 Setup di BancaPiccola

```
cd BancaPiccola-vuln
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
# oppure: source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Apri http://127.0.0.1:5000 → deve apparire la pagina di login di BancaPiccola.

✅ **Hai finito il setup**.

---

<a name="cap4"></a>
## Capitolo 4 — Troubleshooting per il docente

Lista dei **5 errori più frequenti** in aula, con sintomi e soluzione.

### 4.1 "python non è riconosciuto come comando"

**Sintomo**: appena dopo l'installazione di Python, `python --version` dà errore.

**Cause**:
- È stata saltata la checkbox **"Add Python to PATH"** durante l'installazione.
- Il terminale era già aperto prima dell'installazione (non ha la nuova PATH).

**Soluzione**:
1. Chiudi tutti i terminali aperti.
2. Apri un terminale nuovo. Riprova.
3. Se ancora non funziona: disinstalla Python (Pannello di controllo) → reinstallalo spuntando "Add Python to PATH".

### 4.2 "running scripts is disabled" su PowerShell

**Sintomo**: l'attivazione del venv su Windows fallisce con quell'errore.

**Soluzione una tantum**:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Conferma con `S`, poi riprova ad attivare il venv.

### 4.3 "ModuleNotFoundError: No module named 'flask'"

**Sintomo**: `python hello_flask.py` non trova Flask, anche dopo `pip install flask`.

**Causa**: il venv non è attivo. Stai usando il Python globale.

**Soluzione**: verifica che vedi `(.venv)` all'inizio del prompt. Se no, riattivalo:
```
.\.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate      # macOS/Linux
```

### 4.4 Il browser dice "Impossibile raggiungere il sito" su localhost:5000

**Sintomo**: Flask gira ma il browser non si connette.

**Cause possibili**:
- Hai chiuso il terminale dove gira Flask → server spento.
- Antivirus/firewall blocca localhost (raro, ma capita con sicurezza endpoint aziendale).
- Stai accedendo a `https://` invece che `http://` (Flask di default è HTTP).

**Soluzione**: rilancia `python hello_flask.py` e accedi esattamente a `http://127.0.0.1:5000` (non https, non `localhost:5000` se non funziona — usa direttamente l'IP).

### 4.5 VS Code non vede Python

**Sintomo**: in VS Code, il pulsante "Run Python File" non funziona o l'IntelliSense è cieca.

**Soluzione**:
1. `Ctrl+Shift+P` → digita "Python: Select Interpreter"
2. Seleziona quello dentro `.venv/Scripts/python.exe` (Windows) o `.venv/bin/python` (Unix).

In basso a destra in VS Code deve apparire la versione Python con il path al venv.

---

<a name="cap5"></a>
## Capitolo 5 — Verifica di completamento

All'inizio di **M1**, ogni discente deve mostrare nel proprio terminale:

```
1) python --version          → Python 3.12.x
2) (.venv) prompt attivo     → SI
3) pip list | grep -i flask  → flask presente
4) python hello_flask.py     → server parte
5) browser su 127.0.0.1:5000 → vede la pagina
```

Se uno qualsiasi di questi 5 step non funziona, **5-10 minuti di troubleshooting** in aula prima di iniziare M1.

> Se più di 3 discenti su 15 hanno problemi, vale la pena dedicare i primi 20 min di M1 al recupero dell'ambiente. Senza ambiente funzionante, M1 va avanti ma i lab di M2 falliscono in massa.

### Checklist di sopravvivenza per il discente

Stampa e tieni vicino al PC:

```
✅ Python 3.12+ installato (PATH ok)
✅ VS Code con estensione Python
✅ Cartella di lavoro: ~/cybersec-its/
✅ Ambiente virtuale: ~/cybersec-its/.venv/
✅ Flask installato dentro .venv
✅ hello_flask.py funziona

Compito a casa:
✅ Git installato
✅ DB Browser installato
✅ BancaPiccola clonato
✅ BancaPiccola-vuln gira con setup pulito
```

---

<a name="cap6"></a>
## Capitolo 6 — Routine quotidiana del corso

Ogni volta che apri il PC per fare il corso, **questi sono i 3 passi**:

### 1. Apri il terminale e naviga al progetto

```
cd C:\Users\tu\cybersec-its            # Windows
cd ~/cybersec-its                       # macOS/Linux
```

### 2. Attiva il venv

```
.\.venv\Scripts\Activate.ps1            # Windows PowerShell
source .venv/bin/activate                # macOS/Linux
```

Verifica `(.venv)` nel prompt.

### 3. Apri VS Code nella cartella

```
code .
```

Da qui puoi:
- Modificare file dall'editor.
- Eseguire script dal terminale integrato di VS Code (`Ctrl+ò` su Windows, `Ctrl+`` ` su Mac).
- Avere IntelliSense funzionante (perché VS Code "vede" il venv).

### Comandi essenziali da memorizzare

| Comando | Cosa fa |
|---------|---------|
| `pip install nome-libreria` | Installa una libreria Python nel venv |
| `pip list` | Mostra le librerie installate |
| `pip freeze > requirements.txt` | Salva le librerie installate in un file |
| `pip install -r requirements.txt` | Installa tutte le librerie del file |
| `python script.py` | Esegue uno script |
| `deactivate` | Esce dal venv |

---

**Prossimo modulo**: M1 — Fondamenti di Cybersecurity (4h).
Hai l'ambiente pronto. Adesso parliamo davvero di sicurezza.
