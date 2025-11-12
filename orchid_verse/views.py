from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import (
    SiteLogo, 
    CultivatedOrchid,
    OrchidEvent
)
from .forms import OrchidEventForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from datetime import date



# Create your views here.

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
        context = super().get_context_data(**kwargs)
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



# class OrchidDetailView(SeasonalLogoMixin, DetailView):
#     model = Orchid
#     template_name = 'orchid_detail.html'
