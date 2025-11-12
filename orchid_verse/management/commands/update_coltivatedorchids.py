# update_cultivation_data.py
# Popola 
# Usa prima il nickname,
#           [{"nickname": "Phal Marina",
#           "received_from": "Marina Radicella"}]
# in alternativa usa un identificatore stabile 
#           (es. species_id o purchase_id) 
# per trovare la pianta da aggiornare.

import os
import json
from django.core.management.base import BaseCommand
from orchid_verse.models import (
    CultivatedOrchid, 
    OrchidSpecies)
from django.utils.dateparse import parse_date

class Command(BaseCommand):
    help = "Aggiorna solo i campi definiti nel modello CultivatedOrchid."

    def handle(self, *args, **kwargs):
        file_path = os.path.join('orchid_verse', 'data', 'orchids_update.json')

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File non trovato: {file_path}"))
            return

        with open(file_path, encoding='utf-8') as f:
            updates = json.load(f)

        updated = 0

        for entry in updates:
            orchid = None

            # 1. Cerca per nickname
            nickname = entry.get('nickname', '').strip()
            if nickname:
                orchid = CultivatedOrchid.objects.filter(nickname__iexact=nickname).first()

            # 2. Se non trovata, cerca per specie
            if not orchid and entry.get('genus'):
                species = OrchidSpecies.objects.filter(
                    genus=entry.get('genus', '').strip(),
                    species_name=entry.get('species_name', '').strip(),
                    hybrid_name=entry.get('hybrid_name', '').strip()
                ).first()
                if species:
                    orchid = CultivatedOrchid.objects.filter(species=species).first()

            # 3. Se non trovata, cerca per acquisto
            if not orchid and entry.get('purchase_id'):
                orchid = CultivatedOrchid.objects.filter(purchase_id=entry['purchase_id']).first()

            if not orchid:
                continue

            # Aggiorna solo i campi esistenti nel modello
            orchid.nickname = entry.get('nickname', orchid.nickname)
            orchid.purchase_price = entry.get('purchase_price', orchid.purchase_price)
            orchid.identification_level = entry.get('identification_level', orchid.identification_level)
            orchid.origin_type = entry.get('origin_type', orchid.origin_type)
            orchid.received_from = entry.get('received_from', orchid.received_from)
            orchid.received_date = parse_date(entry.get('received_date')) if entry.get('received_date') else orchid.received_date
            orchid.location_type = entry.get('location_type', orchid.location_type)
            orchid.relative_position = entry.get('relative_position', orchid.relative_position)
            orchid.estimated_variation = entry.get('estimated_variation', orchid.estimated_variation)
            orchid.is_alive = entry.get('is_alive', orchid.is_alive)
            orchid.date_of_death = parse_date(entry.get('date_of_death')) if entry.get('date_of_death') else orchid.date_of_death
            orchid.last_watered = parse_date(entry.get('last_watered')) if entry.get('last_watered') else orchid.last_watered
            orchid.cultivation_notes = entry.get('cultivation_notes', orchid.cultivation_notes)

            orchid.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Aggiornate {updated} orchidee coltivate."))




