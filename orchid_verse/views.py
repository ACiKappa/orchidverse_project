from django.views.generic import ListView
from .models import CultivatedOrchid

# Create your views here.

class CultivatedOrchidListView(ListView):
    model = CultivatedOrchid
    template_name = 'orchid_verse/orchid_list.html'
    context_object_name = 'orchids'
