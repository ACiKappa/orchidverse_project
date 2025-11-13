from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import OrchidPurchaseSerializer
from datetime import date
from .models import (
    SiteLogo, 
    OrchidPurchase,
    CultivatedOrchid,
    OrchidEvent,
)
from .forms import OrchidEventForm 

class SeasonalLogoMixin:
    def get_current_season(self):
        month = date.today().month
        if month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'autumn'
        else:
            return 'winter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # type: ignore
        season = self.get_current_season()
        context['season'] = season
        context['logo'] = SiteLogo.objects.filter(season=season).first()
        return context


class HomeView(SeasonalLogoMixin, TemplateView):
    template_name = 'orchid_verse/home.html'

# È una vista "normale" perché non richiede input da parte dell’utente.
class CultivatedOrchidListView(SeasonalLogoMixin, ListView):
    model = CultivatedOrchid
    template_name = 'orchid_verse/orchid_list.html'
    context_object_name = 'orchids'


# class OrchidDetailView(SeasonalLogoMixin, DetailView):
#     model = Orchid
#     template_name = 'orchid_detail.html'


# È una vista "normale" perché non richiede input da parte dell’utente.
class OrchidEventListView(SeasonalLogoMixin, ListView):
    model = OrchidEvent
    template_name = 'orchid_verse/event_list.html'
    context_object_name = 'events'
    ordering = ['-date']

class OrchidEventCreateView(SeasonalLogoMixin, SuccessMessageMixin, CreateView):
    model = OrchidEvent
    form_class = OrchidEventForm
    template_name = 'orchid_verse/event_form.html'
    success_url = reverse_lazy('event_list')  # o altro URL dopo il salvataggio
    success_message = "Evento registrato con successo 🌸"






# API JsonResponse
def api_orchidee_per_genere(request):
    orchids = CultivatedOrchid.objects.select_related('species').all()

    genus_dict = {}

    for orchid in orchids:
        genus = orchid.species.genus if orchid.species and orchid.species.genus else "Genere sconosciuto"
        orchid_info = {
            'id': orchid.id,
            'nickname': orchid.nickname,
            'species': orchid.species.full_name() if orchid.species else None,
            'received_date': orchid.received_date,
            'is_alive': orchid.is_alive,
        }
        genus_dict.setdefault(genus, []).append(orchid_info)

    return JsonResponse({'orchids_by_genus': genus_dict})


# API REST

class OrchidPurchaseViewSet(viewsets.ModelViewSet):
    queryset = OrchidPurchase.objects.all()
    serializer_class = OrchidPurchaseSerializer


# Metodo	Endpoint	Azione
# GET	/api/acquisti/	Lista acquisti
# POST	/api/acquisti/	Crea nuovo acquisto
# GET	/api/acquisti/<id>/	Dettaglio acquisto
# PUT	/api/acquisti/<id>/	Aggiorna completamente
# PATCH	/api/acquisti/<id>/	Aggiorna parzialmente
# DELETE	/api/acquisti/<id>/	Elimina acquisto

