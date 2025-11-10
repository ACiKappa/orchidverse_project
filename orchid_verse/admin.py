from django.contrib import admin
from .models import (
    SiteLogo,
    OrchidSpecies,
    Seller,
    OrchidPurchase,
    CultivatedOrchid,
    OrchidEvent
)
from django.utils.html import format_html


@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    list_display = ('season', 'description', 'image_preview')
    list_filter = ('season',)
    search_fields = ('description',)

    @admin.display(description="Anteprima")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;">', obj.image.url)
        return "Nessuna immagine"


@admin.register(OrchidSpecies)
class OrchidSpeciesAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'is_botanical', 'growth_type', 'temperature_range',
        'light_intensity', 'humidity_preference', 'fertilization_frequency'
    ]
    list_filter = [
        'is_botanical', 'growth_type', 'temperature_range',
        'light_intensity', 'humidity_preference', 'fertilization_frequency'
    ]
    search_fields = ['genus', 'species_name', 'variety', 'hybrid_name', 'origin_zone']
    readonly_fields = ['full_name']
    fieldsets = (
        ('Identificazione', {
            'fields': ('genus', 'species_name', 'variety', 'hybrid_name', 'is_botanical')
        }),
        ('Ecologia e ambiente', {
            'fields': (
                'growth_type', 'temperature_range', 'origin_zone',
                'temperature_min', 'temperature_max',
                'light_intensity', 'humidity_preference', 'prefers_mounting'
            )
        }),
        ('Concimazione e riposo', {
            'fields': (
                'fertilization_frequency',
                'rest_period_start', 'rest_period_end',
                'rest_temperature_min', 'rest_temperature_max'
            )
        }),
        ('Note', {
            'fields': ('notes',)
        }),
    )


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'email', 'phone', 'website']
    search_fields = ['name', 'owner', 'email', 'phone']
    list_filter = ['owner']
    readonly_fields = ['website']
    fieldsets = (
        ('Identità del venditore', {
            'fields': ('name', 'owner')
        }),
        ('Contatti', {
            'fields': ('email', 'phone', 'website', 'address')
        }),
        ('Note e impressioni', {
            'fields': ('notes',)
        }),
    )


class CultivatedOrchidInline(admin.TabularInline):
    model = CultivatedOrchid
    extra = 0
    fields = ['nickname', 'species', 
              'purchase_price', 'origin_type', 
              'received_from', 'received_date']
    show_change_link = True

@admin.register(OrchidPurchase)
class OrchidPurchaseAdmin(admin.ModelAdmin):
    list_display = ['purchase_date', 'seller', 'order_number', 'total_price_display']
    list_filter = ['purchase_date', 'seller']
    search_fields = ['order_number', 'seller__name']
    inlines = [CultivatedOrchidInline]

    @admin.display(description="Totale ordine")
    def total_price_display(self, obj):
        return f"{obj.total_price:.2f} €"

class HasPhotoFilter(admin.SimpleListFilter):
    title = 'Ha foto'
    parameter_name = 'has_photo'

    def lookups(self, request, model_admin):
        return [('yes', 'Sì'), ('no', 'No')]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(photo='')
        elif self.value() == 'no':
            return queryset.filter(photo='')
        return queryset

@admin.register(OrchidEvent)
class OrchidEventAdmin(admin.ModelAdmin):

    @admin.display(description="Foto")
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height: 100px;" />', obj.photo.url)
        return "—"

    list_display = ['orchid', 'event_type', 'date', 
                    'photo_thumbnail', 'description']
    
    list_filter = ['event_type', 'date', HasPhotoFilter]
    autocomplete_fields = ['orchid']
    search_fields = ['orchid__nickname', 'description']
    date_hierarchy = 'date'
    readonly_fields = ('photo',)


class OrchidEventInline(admin.TabularInline):
    model = OrchidEvent
    extra = 0
    fields = ['date', 'event_type', 
              'photo', 'description']
    readonly_fields = ['photo']
    ordering = ['-date']
    show_change_link = True


from .models import CultivatedOrchid

@admin.register(CultivatedOrchid)
class CultivatedOrchidAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'species', 
                    'origin_type', 'purchase_price', 
                    'received_date', 'is_alive']
    list_filter = ['origin_type', 'location_type', 'is_alive']
    search_fields = ['nickname', 'species__genus', 
                     'species__species_name', 'received_from']
    date_hierarchy = 'received_date'
   
    fieldsets = (
        ('Identificazione', {
            'fields': ('nickname', 'species', 
                       'identification_level')
        }),
       ('Ambiente', {
            'fields': ('location_type', 'relative_position', 'estimated_variation')
        }),
        ('Stato Vitale', {
            'fields': ('is_alive', 'date_of_death')
        }),
        ('Cura', {
            'fields': ('last_watered',)
        }),
        ('Note', {
            'fields': ('notes',)
        }),
    )

    inlines = [OrchidEventInline]


# testare il filtro HasPhotoFilter
# migliorare la visualizzazione delle immagini nell’admin


# Se vuoi un’esperienza ancora più fluida, puoi usare autocomplete_fields per i ForeignKey (es. orchid, seller) nei modelli con molti record.
# Per OrchidEvent, potresti aggiungere una inline nel modello CultivatedOrchid per visualizzare gli eventi direttamente nella scheda della pianta.
# Se ti interessa, posso aiutarti a creare anche dei ModelForm personalizzati per validazioni più robuste o suggerimenti dinamici.
# Vuoi che aggiungiamo le inlines o personalizziamo i form?