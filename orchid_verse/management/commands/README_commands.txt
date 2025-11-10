OrchidVerse – Comandi Django Personalizzati
==========================================

📁 Posizione dei comandi:
Tutti i comandi personalizzati si trovano in:
orchid_verse/management/commands/

📁 File JSON richiesto:
orchid_verse/data/sellers.json

------------------------------------------------------------
🟢 Comando: import_sellers
------------------------------------------------------------
Scopo:
Importa venditori dal file sellers.json nel database.

Esecuzione:
python manage.py import_sellers

Funzionalità:
- Legge il file JSON
- Crea nuovi oggetti Seller se non esistono già
- Ignora i duplicati (usa get_or_create)
- Mostra quanti venditori sono stati creati o saltati

------------------------------------------------------------
🟡 Comando: update_sellers (opzionale, da creare)
------------------------------------------------------------
Scopo:
Aggiorna i dati dei venditori esistenti in base al file JSON.

Esecuzione prevista:
python manage.py update_sellers

Funzionalità prevista:
- Cerca venditori esistenti per name
- Aggiorna i campi email, website, phone, address, notes

------------------------------------------------------------
🔵 Comando: export_sellers (opzionale, da creare)
------------------------------------------------------------
Scopo:
Esporta tutti i venditori in un file JSON per backup o condivisione.

Esecuzione prevista:
python manage.py export_sellers

Funzionalità prevista:
- Legge tutti gli oggetti Seller
- Scrive un file sellers_exported.json con i campi principali

------------------------------------------------------------
🧪 Test e help
------------------------------------------------------------
Per testare un comando:
python manage.py <nome_comando>

Per vedere la guida di un comando:
python manage.py <nome_comando> --help

------------------------------------------------------------
📦 Suggerimenti
------------------------------------------------------------
- Mantieni sellers.json aggiornato e ben formattato
- Usa comandi personalizzati per sincronizzare, esportare e gestire i dati
- Puoi estendere i comandi per gestire altri modelli (es. CultivatedOrchid, OrchidEvent)

------------------------------------------------------------
🌿 OrchidVerse – Botanica, narrativa e codice
------------------------------------------------------------
