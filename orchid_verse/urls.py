
from django.urls import path
from django.views.generic import TemplateView
from .views import CultivatedOrchidListView

urlpatterns = [
    path('', TemplateView.as_view(template_name='orchid_verse/home.html'), name='home'),
    path('orchids/', CultivatedOrchidListView.as_view(), name='orchid_list'),
]
