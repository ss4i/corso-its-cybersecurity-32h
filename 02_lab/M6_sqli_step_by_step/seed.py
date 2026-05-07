"""Inizializza il DB SQLite con dati di esempio per il lab."""
import os
import sqlite3

DB = "banca.db"

if os.path.exists(DB):
    os.remove(DB)

conn = sqlite3.connect(DB)
with open("schema.sql") as f:
    conn.executescript(f.read())

# Utenti (password volutamente in chiaro per il lab — si fa hashing in M6.4)
users = [
    ("alice@bank.it", "alice_pass", 1500.0),
    ("bob@bank.it", "bob_pass", 2300.0),
    ("admin@bank.it", "Sup3rS3gr3t0!", 999999.0),
]
conn.executemany(
    "INSERT INTO users (email, password, saldo) VALUES (?, ?, ?)",
    users,
)

# Messaggi che NON dovremmo poter vedere via SQLi
messaggi = [
    ("La combinazione della cassaforte è 4815-1623",),
    ("Il piano di marketing 2027 è in /docs/strategia.pdf",),
]
conn.executemany(
    "INSERT INTO messaggi_segreti (contenuto) VALUES (?)",
    messaggi,
)

conn.commit()
conn.close()

print(f"✅ DB '{DB}' creato.")
print(f"   - {len(users)} utenti")
print(f"   - {len(messaggi)} messaggi segreti")
print(f"\nUtenti di test:")
for email, pwd, saldo in users:
    print(f"   {email} / {pwd}  → saldo {saldo} €")
