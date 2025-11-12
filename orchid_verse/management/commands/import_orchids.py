import os
import json
from django.core.management.base import BaseCommand
from orchid_verse.models import (
    Seller, 
    OrchidPurchase, 
    OrchidSpecies, 
    CultivatedOrchid
)
from django.utils.dateparse import parse_date
from decimal import Decimal

'''
JSON
    Caso singola orchidea
        con Seller
        senza Seller
    Caso con Seller e lista di orchidee

Popola:
    OrchidSpecies con:
        genus
        species_name
        variety
        hybrid_name
        is_botanical

    OrchidPurchase con:
    (solo se c'è un seller)
        seller
        origin='acquisto'

    CultivatedOrchid con:
        species
        purchase
        notes
        is_alive=True
    
Altri:

Per i venditori di fiducia:
    Usare import_sellers.py

Per i dati colturali:
    Usare update_cultivatedorchids.py

Per schede di coltivazione:
    Usare update_OrchidSpecies.py



Da fare:
    Validare i dati prima dell'update
    Segnalare le orchidee non trovate
    Generare un file CSV di revisione    
'''

class Command(BaseCommand):
    help = "Importa orchidee da JSON e popola i modelli Seller, OrchidPurchase, OrchidSpecies, CultivatedOrchid."

    def add_arguments(self, parser):
        parser.add_argument('json_path', type=str, help='Percorso al file JSON da importare')

    def handle(self, *args, **options):
        file_path = options['json_path']

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File non trovato: {file_path}"))
            return

        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)

        total_orchids = 0
        imported_orchids = 0
        skipped_orchids = 0

        for entry in data:
            seller_obj = None
            if entry.get('seller'):
                seller_obj, _ = Seller.objects.get_or_create(name=entry['seller'])

            # Caso con lista di orchidee
            if 'orchids' in entry:
                raw_date = entry.get('purchase_date')
                purchase_date = parse_date(str(raw_date)) if raw_date else None
                if not purchase_date:
                    self.stderr.write(self.style.WARNING(
                        f"⚠️ Nessuna purchase_date per seller '{entry.get('seller')}'. Uso data simbolica 1900-01-01."
                    ))
                    purchase_date = parse_date("1900-01-01")
                                
                actual_total_price = entry.get('actual_total_price')
                if actual_total_price is not None:
                    actual_total_price = Decimal(str(actual_total_price))
                else:
                    actual_total_price = Decimal('0.00')

                purchase_obj, created = OrchidPurchase.objects.get_or_create(
                    seller=seller_obj,
                    purchase_date=purchase_date,
                    defaults={'actual_total_price': actual_total_price}
                )

                seller_name = seller_obj.name if seller_obj else "nessun seller"

                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"🧾 Nuovo acquisto creato: {seller_name} - {purchase_date}"
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"🔁 Acquisto già esistente: {seller_name} - {purchase_date}"
                    ))


                for orchid_data in entry['orchids']:
                    total_orchids += 1
                    if self.import_orchid(orchid_data, purchase_obj):
                        imported_orchids += 1
                    else:
                        skipped_orchids += 1

            # Caso singola orchidea
            else:
                raw_date = entry.get('purchase_date')
                purchase_date = parse_date(str(raw_date)) if raw_date else None
                if seller_obj:
                    if not purchase_date:
                        self.stderr.write(self.style.WARNING(
                            f"⚠️ Orchidea con seller '{seller_obj.name}' ma senza purchase_date. Uso data simbolica 1900-01-01."
                        ))
                        purchase_date = parse_date("1900-01-01")

                    purchase_obj = OrchidPurchase.objects.create(
                        seller=seller_obj,
                        purchase_date=purchase_date,
                        actual_total_price=entry.get('actual_total_price')
                    )
                else:
                    purchase_obj = None

                total_orchids += 1
                if self.import_orchid(entry, purchase_obj):
                    imported_orchids += 1
                else:
                    skipped_orchids += 1

        self.stdout.write(self.style.SUCCESS(
            f"Orchidee nel JSON: {total_orchids} | Già presenti: {skipped_orchids} | Importate: {imported_orchids}"
        ))

    def import_orchid(self, data, purchase_obj):
        genus = data.get('genus', '').strip()
        species_name = data.get('species_name', '').strip()
        hybrid_name = data.get('hybrid_name', '').strip()
        nickname = data.get('nickname', '').strip()

        # Chiave di identificazione
        if genus or species_name or hybrid_name:
            exists = CultivatedOrchid.objects.filter(
                species__genus=genus,
                species__species_name=species_name,
                species__hybrid_name=hybrid_name
            ).exists()
        else:
            if not nickname:
                self.stderr.write(self.style.ERROR(
                    f"❌ Orchidea senza identificazione né nickname. Salto."
                ))
                return False
            exists = CultivatedOrchid.objects.filter(nickname=nickname).exists()

        if exists:
            self.stderr.write(self.style.WARNING(
                f"🔁 Orchidea già presente: {genus} {species_name} {hybrid_name} / {nickname}"
            ))
            return False

        species_obj, _ = OrchidSpecies.objects.get_or_create(
            genus=genus,
            species_name=species_name,
            variety=data.get('variety', '').strip(),
            hybrid_name=hybrid_name,
            is_botanical=data.get('is_botanical', False),
            growth_type=data.get('growth_type', '').strip()
        )

        if purchase_obj:
            origin_type = 'purchase'
            received_from = None
            received_date = None
        else:
            origin_type = data.get('origin_type', 'unknown')
            received_from = data.get('received_from', '').strip() or 'sconosciuto'
            received_date = parse_date(str(data.get('received_date'))) if data.get('received_date') else None

        identification_level = data.get('identification_level') or 'unknown'

        CultivatedOrchid.objects.create(
            species=species_obj,
            purchase=purchase_obj,
            notes=data.get('notes', ''),
            is_alive=True,
            purchase_price=data.get('purchase_price'),
            identification_level=identification_level,
            nickname=nickname,
            origin_type=origin_type,
            received_from=received_from,
            received_date=received_date
        )

        return True

# python manage.py import_orchids orchid_verse/data/orchids.json


# Le informazioni sono incomplete o soggette a revisione
# Magari si sta importando da fonti diverse 
# (es. JSON iniziale vs schede di coltivazione).

# Alcuni campi
# potrebbero arrivare in un secondo momento 
# da un file aggiornato, da un'interfaccia admin, 
# o da un modulo di revisione.