import os
import json
from django.core.management.base import BaseCommand
from orchid_verse.models import (
    Seller, 
    OrchidPurchase, 
    OrchidSpecies, 
    CultivatedOrchid)
from django.utils.dateparse import parse_date
from decimal import Decimal

class Command(BaseCommand):
    help = "Importa orchidee da JSON e " \
    "popola i modelli Seller, OrchidPurchase, OrchidSpecies, CultivatedOrchid."

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
            purchase_obj = None

            if entry.get('seller'):
                seller_obj, _ = Seller.objects.get_or_create(name=entry['seller'])

            if 'orchids' in entry:
                purchase_date = parse_date(str(entry.get('purchase_date'))) or parse_date("1900-01-01")
                actual_total_price = Decimal(str(entry.get('actual_total_price') or '0.00'))

                if seller_obj:
                    purchase_obj, _ = OrchidPurchase.objects.get_or_create(
                        seller=seller_obj,
                        purchase_date=purchase_date,
                        defaults={'actual_total_price': actual_total_price}
                    )

                for orchid_data in entry['orchids']:
                    total_orchids += 1
                    if self.import_orchid(orchid_data, purchase_obj):
                        imported_orchids += 1
                    else:
                        skipped_orchids += 1
            else:
                purchase_date = parse_date(str(entry.get('purchase_date'))) or parse_date("1900-01-01")
                actual_total_price = Decimal(str(entry.get('actual_total_price') or '0.00'))

                if seller_obj:
                    purchase_obj, _ = OrchidPurchase.objects.get_or_create(
                        seller=seller_obj,
                        purchase_date=purchase_date,
                        defaults={'actual_total_price': actual_total_price}
                    )

                total_orchids += 1
                if self.import_orchid(entry, purchase_obj):
                    imported_orchids += 1
                else:
                    skipped_orchids += 1

        self.stdout.write(self.style.SUCCESS(
            f"🌸 Orchidee nel JSON: {total_orchids} | Importate: {imported_orchids} | Saltate: {skipped_orchids}"
        ))

    def import_orchid(self, data, purchase_obj):
        genus = data.get('genus', '').strip()
        species_name = data.get('species_name', '').strip()
        hybrid_name = data.get('hybrid_name', '').strip()
        nickname = data.get('nickname', '').strip()

        if not (genus or species_name or hybrid_name or nickname):
            self.stderr.write(self.style.ERROR("❌ Orchidea senza identificazione né nickname. Salto."))
            return False

        # Identificazione species
        if genus and hybrid_name == "ibrido commerciale":
            species_obj, _ = OrchidSpecies.objects.get_or_create(
                genus=genus,
                hybrid_name="ibrido commerciale",
                defaults={'species_name': '', 'variety': '', 'is_botanical': False, 'growth_type': ''}
            )
        elif genus or species_name or hybrid_name:
            species_obj, _ = OrchidSpecies.objects.get_or_create(
                genus=genus,
                species_name=species_name,
                hybrid_name=hybrid_name,
                variety=data.get('variety', '').strip(),
                is_botanical=data.get('is_botanical', False),
                growth_type=data.get('growth_type', '').strip()
            )
        else:
            species_obj, _ = OrchidSpecies.objects.get_or_create(
                genus='Generica',
                species_name='',
                hybrid_name='',
                variety='',
                is_botanical=False,
                growth_type=''
            )

        # Controllo duplicati
        orchid_qs = CultivatedOrchid.objects.filter(species=species_obj)
        if nickname:
            orchid_qs = orchid_qs.filter(nickname=nickname)
        if orchid_qs.exists():
            self.stderr.write(self.style.WARNING(f"🔁 Orchidea già presente: {genus} {species_name} {hybrid_name} / {nickname}"))
            return False

        # Origine
        if purchase_obj:
            origin_type = 'purchase'
            received_from = None
            received_date = None
        else:
            origin_type = data.get('origin_type', 'unknown')
            received_from = data.get('received_from', '').strip() or 'sconosciuto'
            received_date = parse_date(str(data.get('received_date'))) if data.get('received_date') else None

        CultivatedOrchid.objects.create(
            species=species_obj,
            purchase=purchase_obj,
            cultivation_notes=data.get('cultivation_notes', ''),
            is_alive=True,
            purchase_price=data.get('purchase_price'),
            identification_level=data.get('identification_level', 'unknown'),
            nickname=nickname,
            origin_type=origin_type,
            received_from=received_from,
            received_date=received_date
        )

        self.stdout.write(self.style.SUCCESS(f"✅ Importata: {nickname or genus + ' ' + species_name}"))
        return True
