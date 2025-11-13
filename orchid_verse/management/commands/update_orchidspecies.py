import os
import json
from django.core.management.base import BaseCommand
from orchid_verse.models import OrchidSpecies

class Command(BaseCommand):
    help = "Aggiorna e popola OrchidSpecies da un file JSON con dati completi."

    def add_arguments(self, parser):
        parser.add_argument('json_path', type=str, help='Percorso al file JSON da importare')

    def handle(self, *args, **options):
        file_path = options['json_path']
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File non trovato: {file_path}"))
            return

        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)

        total_species = 0
        updated_species = 0
        created_species = 0
        skipped_species = 0

        for entry in data:
            total_species += 1
            if self.update_species(entry):
                updated_species += 1
            else:
                skipped_species += 1

        self.stdout.write(self.style.SUCCESS(
            f"🌱 OrchidSpecies nel JSON: {total_species} | Aggiornate/Importate: {updated_species} | Saltate: {skipped_species}"
        ))

    def update_species(self, data):
        genus = data.get('genus', '').strip()
        species_name = data.get('species_name', '').strip()
        hybrid_name = data.get('hybrid_name', '').strip()
        variety = data.get('variety', '').strip()

        if not genus:
            self.stderr.write(self.style.ERROR("❌ Specie senza genus. Salto."))
            return False

        # Trova o crea OrchidSpecies
        species_obj, created = OrchidSpecies.objects.get_or_create(
            genus=genus,
            species_name=species_name,
            hybrid_name=hybrid_name,
            variety=variety,
            defaults={
                'is_botanical': data.get('is_botanical', True),
                'growth_type': data.get('growth_type', 'unknown'),
                'temperature_range': data.get('temperature_range', 'unknown'),
                'origin_zone': data.get('origin_zone', ''),
                'temperature_min': data.get('temperature_min'),
                'temperature_max': data.get('temperature_max'),
                'light_intensity': data.get('light_intensity', 'medium'),
                'humidity_preference': data.get('humidity_preference', 'moderate'),
                'prefers_mounting': data.get('prefers_mounting', False),
                'fertilization_frequency': data.get('fertilization_frequency', 'unknown'),
                'rest_period_start': data.get('rest_period_start', ''),
                'rest_period_end': data.get('rest_period_end', ''),
                'rest_temperature_min': data.get('rest_temperature_min'),
                'rest_temperature_max': data.get('rest_temperature_max'),
                'botanical_notes': data.get('botanical_notes', '')
            }
        )

        if not created:
            # Aggiorna i campi esistenti
            species_obj.is_botanical = data.get('is_botanical', species_obj.is_botanical)
            species_obj.growth_type = data.get('growth_type', species_obj.growth_type)
            species_obj.temperature_range = data.get('temperature_range', species_obj.temperature_range)
            species_obj.origin_zone = data.get('origin_zone', species_obj.origin_zone)
            species_obj.temperature_min = data.get('temperature_min', species_obj.temperature_min)
            species_obj.temperature_max = data.get('temperature_max', species_obj.temperature_max)
            species_obj.light_intensity = data.get('light_intensity', species_obj.light_intensity)
            species_obj.humidity_preference = data.get('humidity_preference', species_obj.humidity_preference)
            species_obj.prefers_mounting = data.get('prefers_mounting', species_obj.prefers_mounting)
            species_obj.fertilization_frequency = data.get('fertilization_frequency', species_obj.fertilization_frequency)
            species_obj.rest_period_start = data.get('rest_period_start', species_obj.rest_period_start)
            species_obj.rest_period_end = data.get('rest_period_end', species_obj.rest_period_end)
            species_obj.rest_temperature_min = data.get('rest_temperature_min', species_obj.rest_temperature_min)
            species_obj.rest_temperature_max = data.get('rest_temperature_max', species_obj.rest_temperature_max)
            species_obj.botanical_notes = data.get('botanical_notes', species_obj.botanical_notes)
            species_obj.save()
            self.stdout.write(self.style.SUCCESS(f"🔄 Aggiornata specie: {species_obj.full_name()}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"✅ Creata nuova specie: {species_obj.full_name()}"))

        return True
