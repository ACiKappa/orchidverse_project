import json
import os
from django.core.management.base import BaseCommand
from orchid_verse.models import Seller

class Command(BaseCommand):
    help = 'Importa venditori da un file JSON'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('orchid_verse', 'data', 'sellers.json')

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File non trovato: {file_path}"))
            return

        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)

        created, skipped = 0, 0
        for entry in data:
            obj, was_created = Seller.objects.get_or_create(
                name=entry['name'],
                defaults={
                    'email': entry.get('email', ''),
                    'website': entry.get('website', ''),
                    'phone': entry.get('phone', ''),
                    'address': entry.get('address', ''),
                    'notes': entry.get('notes', '')
                }
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f"{created} venditori importati. {skipped} già esistenti."))
