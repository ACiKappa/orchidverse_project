from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import TextChoices



# Create your models here.

# ┌────────────────────┐
# │   OrchidSpecies    │
# └────────┬───────────┘
#          ▼
# ┌────────────────────┐
# │  OrchidPurchase    │◄──────────┐   # acquisto
# └────────┬───────────┘           │
#          ▼                       │
# ┌────────────────────┐           │
# │ CultivatedOrchid   │───────────┘   # pianta reale
# └────────┬───────────┘
#          ▼
# ┌────────────────────┐
# │   OrchidEvent      │              # fioritura, divisione
# └────────────────────┘

# ┌────────────────────┐
# │      Seller        │──────┐
# └────────────────────┘      │
#                             ▼
#                    OrchidPurchase


class OrchidSpecies(models.Model):
    '''
    Modello `OrchidSpecies`: Classificazione botanica e preferenze ambientali.
    Supporta anche identificazioni parziali o generiche.
    '''
    genus = models.CharField(max_length=100)  # es. "Dendrobium"
    species_name = models.CharField(max_length=100, blank=True)  # es. "nobile"
    variety = models.CharField(max_length=100, blank=True)  # es. "var. alba"
    hybrid_name = models.CharField(max_length=200, blank=True)  # es. "Phal. Sogo Yukidian"
    is_botanical = models.BooleanField(default=True)

    # Classificazione ecologica
    growth_type = models.CharField(
        max_length=50,
        choices=[
            ('epiphyte', 'Epifita'),
            ('terrestrial', 'Terrestre'),
            ('lithophyte', 'Litofita'),
            ('mixed', 'Mista'),
            ('unknown', 'Sconosciuta')
        ],
        default='unknown'
    )
    temperature_range = models.CharField(
        max_length=50,
        choices=[
            ('warm', 'Calda'),
            ('intermediate', 'Intermedia'),
            ('cool', 'Fresca'),
            ('cool-intermediate', 'Fresca-Intermedia'),
            ('intermediate-warm', 'Intermedia-Calda'),
            ('unknown', 'Sconosciuta')
        ],
        default='unknown'
    )

    # Esigenze ambientali
    origin_zone = models.CharField(max_length=100, blank=True)
        
    temperature_min = models.FloatField(null=True, blank=True)
    temperature_max = models.FloatField(null=True, blank=True)

    # Le Phalaenopsis prosperano con 1.000–2.000 lux, 
    # mentre le Cattleya e Dendrobium richiedono 3.000–6.000 lux.
    LIGHT_CHOICES = [
        ('low', 'Bassa'),
        ('medium', 'Media'),
        ('high', 'Alta'),
    ]
    light_intensity = models.CharField(
        max_length=50,
        choices=LIGHT_CHOICES,
        help_text="Bassa (500–1.500 lux), Media (1.500–5.000 lux), Alta (5.000–10.000 lux)"
    )

    # Le orchidee epifite (es. Phalaenopsis, Cattleya) preferiscono spesso 60–80%,
    # mentre le terrestri possono tollerare 50–60%.
    HUMIDITY_CHOICES = [
        ('dry', 'Secco'),
        ('moderate', 'Moderato'),
        ('humid', 'Umido'),
    ]
    humidity_preference = models.CharField(
        max_length=50,
        choices=HUMIDITY_CHOICES,
        help_text="Secco (<50%), Moderato (50–70%), Umido (>70%)"
    )

    prefers_mounting = models.BooleanField(default=False)
    
    FERTILIZATION_CHOICES = [
        ('weekly', 'Settimanale'),
        ('biweekly', 'Ogni due settimane'),
        ('monthly', 'Mensile'),
        ('growth_only', 'Solo durante la crescita'),
        ('custom', 'Personalizzato'),
        ('unknown', 'Sconosciuto'),
    ]

    fertilization_frequency = models.CharField(
        max_length=50,
        choices=FERTILIZATION_CHOICES,
        default='unknown',
        help_text="Frequenza di concimazione: es. settimanale, mensile, solo durante la crescita"
    )

    # Settimanale: comune per orchidee in crescita attiva.
    # Mensile: usato per piante più sensibili o in condizioni stabili.
    # Solo durante la crescita: utile per specie con riposo marcato.
    # Personalizzato: se segui un regime specifico (es. alternato, diluito).
    # Sconosciuto: per piante non ancora osservate o identificate.

    #Creare una logica che suggerisce la frequenza ideale 
    # in base alla specie e alla stagione
    # i creare una funzione che suggerisce la concimazione ideale in base a:
        # temperature_range
        # growth_type
        # rest_period_start / end

    rest_period_start = models.CharField(max_length=20, blank=True)
    rest_period_end = models.CharField(max_length=20, blank=True)
    rest_temperature_min = models.FloatField(null=True, blank=True)
    rest_temperature_max = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        '''
        Restituisce un nome descrittivo completo, anche se parziale.
        '''
        if self.hybrid_name:
            return self.hybrid_name
        name = self.genus or "?"
        if self.species_name:
            name += f" {self.species_name}"
        if self.variety:
            name += f" {self.variety}"
        return name

class Seller(models.Model):
    '''
    Modello `Seller`: informazioni sul venditore.
    Può essere collegato a più acquisti.
    '''
    name = models.CharField(max_length=100)  # es. "Orchideria di Morosolo"
    owner = models.CharField(max_length=100, blank=True)  # es. "Edmondo Pozzi"
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)  # es. qualità, packaging, varietà disponibili

    def __str__(self):
        return self.name


class OrchidPurchase(models.Model):
    '''
    Modello `OrchidPurchase`: traccia informazioni sull'acquisto di una pianta.
    Include venditore, contatti, data, prezzo e note.
    '''
    # orchid = models.ForeignKey(OrchidSpecies, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateField()
    # purchase_price = models.DecimalField(max_digits=7, decimal_places=2)  # es. 35.50 €
    order_number = models.CharField(max_length=100, blank=True)
    # plant_photo = models.ImageField(upload_to='orchid_photos/', blank=True, null=True)
    receipt_photo = models.ImageField(upload_to='purchase_receipts/', blank=True, null=True)
    additional_notes = models.TextField(blank=True)

    @property
    def total_price(self):
        '''
        Calcola il prezzo totale dell'ordine sommando 
        i prezzi individuali delle piante collegate.
        '''
        from django.db.models import Sum
        result = self.cultivated_orchids.aggregate(Sum('purchase_price'))
        return f"{result['purchase_price__sum'] or 0:.2f} €"

    def __str__(self):
        count = self.cultivated_orchids.count()
        return f"Ordine di {count} piante, da {self.seller.name if self.seller else 'Venditore sconosciuto'} il {self.purchase_date}"


class CultivatedOrchid(models.Model):
    '''
    Modello `CultivatedOrchid`: 
    Questo modello registra dove 
    e come viene coltivata una pianta specifica.
    Può essere collegata a una specie botanica 
    oppure identificata solo tramite nickname.
    '''
    species = models.ForeignKey(OrchidSpecies, on_delete=models.SET_NULL, null=True, blank=True)
    nickname = models.CharField(max_length=100, blank=True)
    purchase = models.ForeignKey(
        OrchidPurchase, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='cultivated_orchids'
    )
    purchase_price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Prezzo individuale della pianta, se noto"
    )

    identification_level = models.CharField(
        max_length=50,
        choices=[
            ('full', 'Identificazione completa'),
            ('partial', 'Solo genere noto'),
            ('unknown', 'Non identificata')
        ],
        default='unknown'
    )
     
    ORIGIN_CHOICES = [
        ('purchase', 'Acquisto'),
        ('gift', 'Regalo'),
        ('exchange', 'Scambio'),
        ('unknown', 'Sconosciuta')
    ]

    origin_type = models.CharField(max_length=20, choices=ORIGIN_CHOICES, default='purchase')
    # purchase = models.ForeignKey(OrchidPurchase, on_delete=models.SET_NULL, null=True, blank=True)
    received_from = models.CharField(max_length=100, blank=True)  # es. "Marina"
    received_date = models.DateField(null=True, blank=True)

    # Posizione e ambiente
    location_type = models.CharField(
        max_length=50,
        choices=[
            ('home', 'Casa'),
            ('greenhouse', 'Serra'),
            ('outdoor', 'Esterno'),
            ('other', 'Altro')
        ],
        default='home'
    )

    relative_position = models.CharField(
        max_length=100, blank=True,       
        help_text="Descrizione della posizione nella serra o casa (es. 'zona ombra, scaffale alto')"
    )

    estimated_variation = models.TextField(
        blank=True,
        help_text="Annotazioni sulle variazioni ambientali rispetto alla media (es. 'riceve meno luce e più umidità')"
    )
    
    # Stato vitale
    is_alive = models.BooleanField(default=True)
    date_of_death = models.DateField(null=True, blank=True)

    # Cura
    last_watered = models.DateField(
        null=True, blank=True, 
        help_text="Data dell'ultima irrigazione"
    )

    # Note generali
    notes = models.TextField(blank=True)

    
    # Django chiama clean() solo quando usi ModelForm o full_clean() manualmente.
    # Se vuoi che venga eseguito anche in admin, 
    # puoi sovrascrivere save_model() oppure usare ModelForm personalizzato.
    def clean(self):
        if not self.nickname and not self.species:
            raise ValidationError("Devi fornire almeno un nickname o una specie.")

    def __str__(self):
        if self.nickname and self.species:
            return f"{self.nickname} ({self.species.full_name()})"
        elif self.species:
            return self.species.full_name()
        return self.nickname or "Orchidea non identificata"
    
    class Meta:
        ordering = ['received_date']

class EventType(TextChoices):
    BLOOM = 'bloom', 'Fioritura'
    GROWTH = 'growth', 'Nuova crescita'
    ROOTING = 'rooting', 'Radicazione'
    REPOTTING = 'repotting', 'Rinvaso'
    DIVISION = 'division', 'Divisione'
    MOUNTING = 'mounting', 'Nuova zattera'
    PROBLEM = 'problem', 'Problema'
    OTHER = 'other', 'Altro'

class OrchidEvent(models.Model):
    '''
    Modello `OrchidEvent`: documenta visivamente la crescita o eventi di una pianta.
    '''
    orchid = models.ForeignKey(CultivatedOrchid, on_delete=models.CASCADE, related_name='events')
    photo = models.ImageField(upload_to='orchid_gallery/', blank=True, null=True)
    date = models.DateField()
    
    event_type = models.CharField(
        max_length=50,
        choices=EventType.choices,
        default=EventType.OTHER
    )

    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-date'] # mostra prima gli eventi piu recenti

    def clean(self):
        if self.date > timezone.now().date():
            raise ValidationError("La data dell'evento non può essere nel futuro.")
    
    def __str__(self):
        return f"{self.orchid} - {self.event_type} ({self.date})"
    
