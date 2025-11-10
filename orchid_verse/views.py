from django.views.generic import ListView
from django.views.generic import TemplateView
from .models import (
    SiteLogo, 
    CultivatedOrchid
)
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


class CultivatedOrchidListView(SeasonalLogoMixin, ListView):
    model = CultivatedOrchid
    template_name = 'orchid_verse/orchid_list.html'
    context_object_name = 'orchids'


# class OrchidDetailView(SeasonalLogoMixin, DetailView):
#     model = Orchid
#     template_name = 'orchid_detail.html'
