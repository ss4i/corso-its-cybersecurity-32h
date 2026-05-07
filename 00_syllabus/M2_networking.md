# M2 — Networking & ISO/OSI (6h)

## Obiettivo

Al termine del modulo il discente sa:

1. Descrivere i **7 livelli ISO/OSI** e mapparli al modello **TCP/IP** a 4 livelli.
2. Spiegare cosa fa ogni livello con un'analogia (sistema postale, telefonate, ecc.).
3. Riconoscere a vista i protocolli principali: Ethernet, ARP, IP, ICMP, TCP, UDP, DNS, TLS, HTTP, DHCP.
4. Identificare **almeno 2 vulnerabilità per ogni livello** L2-L7 e capire perché esistono.
5. Usare **Wireshark** per catturare e leggere traffico di rete reale.
6. Scrivere in **Python** un client TCP, un mini server, un port scanner e uno sniffer di pacchetti.
7. Capire il **three-way handshake TCP** osservandolo dal vivo in Wireshark.

## Materiale di riferimento

- Materiale nuovo: `01_materiali/M2_networking_isoosi.md` (dispensa completa creata per questo corso)
- `OSPF_Dispensa_ITS.docx` per riferimenti su protocolli di routing (cenno a fine modulo)

## Articolazione oraria

### Sessione 1 — Teoria + L1-L4 (3h)

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:20 | **2.1 Cos'è una rete** — analogia del sistema postale. Mittente, destinatario, busta, percorso, smistamento. | Frontale |
| 0:20 – 0:50 | **2.2 ISO/OSI vs TCP/IP** — i due modelli a confronto. Perché ne studiamo uno teorico e uno pratico. Tabella completa dei 7+4 livelli. | Frontale |
| 0:50 – 1:15 | **2.3 Livello 1 (Fisico) e Livello 2 (Data Link)** — cavi, segnali, MAC address, frame Ethernet, switch. | Frontale |
| 1:15 – 1:30 | **PAUSA** | |
| 1:30 – 2:00 | **2.4 ARP** — come si scopre il MAC dal IP. **Vulnerabilità: ARP spoofing**. Demo con `arp -a`. | Frontale + demo |
| 2:00 – 2:30 | **2.5 Livello 3 (Network)** — IP, subnetting (cenni), routing, ICMP. **Vulnerabilità: IP spoofing, ICMP flood, ping of death**. | Frontale |
| 2:30 – 3:00 | **2.6 Livello 4 (Transport)** — TCP vs UDP, porte, three-way handshake disegnato passo-passo. **Vulnerabilità: SYN flood, port scanning, TCP hijacking**. | Frontale + lavagna |

### Sessione 2 — Lab Wireshark + Python L5-L7 (3h)

| Tempo | Argomento | Modalità |
|-------|-----------|----------|
| 0:00 – 0:15 | **2.7 Installazione Wireshark** — overview interfaccia, filtri base. | Frontale |
| 0:15 – 1:00 | **Lab M2.1 — Wireshark Discovery (45 min)** — Cattura mentre apri `example.com`. Identifica: DNS query, three-way handshake TCP, GET HTTP, risposta. | **Lab guidato** |
| 1:00 – 1:30 | **Lab M2.2 — Socket Python (30 min)** — Scrivi un client TCP che si connette a `example.com:80` e fa una GET manuale. Vedi la stessa cosa in Wireshark. | **Lab guidato** |
| 1:30 – 1:45 | **PAUSA** | |
| 1:45 – 2:00 | **2.8 Livello 5-6-7** — Sessione, presentazione, applicazione. DNS, TLS, HTTP, SMTP. **Vulnerabilità: DNS poisoning, TLS downgrade, application-layer attacks**. | Frontale |
| 2:00 – 2:30 | **Lab M2.3 — Port Scanner Python (30 min)** — Scrivi un mini scanner che testa una lista di porte su `127.0.0.1`. Confronta output con `nmap` (cenno). | **Lab guidato** |
| 2:30 – 2:50 | **Lab M2.4 — Scapy Sniffer (20 min)** — Cattura pacchetti dalla tua interfaccia con `scapy.sniff()` e stampa source/dest/protocollo. | **Lab guidato** |
| 2:50 – 3:00 | **Sintesi finale** — la security in rete è layered: ogni livello ha le sue vulnerabilità e le sue difese. | Frontale |

## Lab del modulo (3h totali)

| Lab | Durata | Output | File |
|-----|--------|--------|------|
| M2.1 | 45 min | Cattura `.pcapng` annotata | `02_lab/M2.1_wireshark_capture.md` |
| M2.2 | 30 min | Client TCP che fa GET manuale | `02_lab/M2.2_socket_tcp.py` |
| M2.3 | 30 min | Port scanner con timeout configurabile | `02_lab/M2.3_port_scanner.py` |
| M2.4 | 20 min | Sniffer scapy con filtro BPF | `02_lab/M2.4_scapy_sniff.py` |

## Verifica

Domande di autovalutazione (entrano in V1):

- Disegna la pila ISO/OSI e indica per ogni livello almeno un protocollo e una vulnerabilità.
- Cosa succede tra "premo Invio dopo aver scritto google.com" e "vedo la pagina"? Indica i livelli coinvolti.
- Cos'è un three-way handshake? Disegnalo.
- Differenza TCP vs UDP — quando si usa l'uno e quando l'altro?
- Cos'è ARP spoofing? Quale livello attacca? Come si difende?

## Note operative

- **Wireshark deve essere preinstallato** il giorno prima (è pesante e a volte richiede driver come Npcap/WinPcap). Istruzioni nel materiale M2.
- **scapy richiede privilegi root/admin** per sniffing. Su Windows: terminale come amministratore. Su macOS/Linux: `sudo`. In aula concordare prima.
- **Attenzione legale**: lo sniffing si fa **solo sulla propria macchina o su rete didattica isolata**. Mai in reti pubbliche o aziendali senza autorizzazione. Da ribadire **due volte** durante il modulo.

## Errori da evitare in classe

- **Non perdersi nel subnetting** — è importante, ma 6 ore non bastano per fare networking serio. Si dà l'idea, si rimanda alla dispensa OSPF chi vuole approfondire.
- **Non saltare l'analogia postale** — la rete è invisibile, l'analogia è l'unico modo per renderla concreta a chi parte da zero.
- **Non far girare scapy in WSL2 senza configurare il network mode** — fallisce silenziosamente. Su Windows usare PowerShell admin.
