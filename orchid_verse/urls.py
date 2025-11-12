
from django.urls import path
#from django.views.generic import TemplateView
from django.urls import path
from .views import (
    HomeView,
    CultivatedOrchidListView,
    OrchidEventListView,
    OrchidEventCreateView)

urlpatterns = [
   # path('', TemplateView.as_view(template_name='orchid_verse/home.html'), name='home'),
    path('', HomeView.as_view(), name='home'),
    path('orchids/', CultivatedOrchidListView.as_view(), name='orchid_list'),
    path('eventi/', OrchidEventListView.as_view(), name='event_list'),
    path('eventi/nuovo/', OrchidEventCreateView.as_view(), name='event_create'),
]




