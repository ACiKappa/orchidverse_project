#from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    HomeView,
    CultivatedOrchidListView,
    OrchidEventListView,
    OrchidEventCreateView,
)
from .views import (
    api_orchidee_per_genere,
    OrchidPurchaseViewSet,
)

urlpatterns = [
   # path('', TemplateView.as_view(template_name='orchid_verse/home.html'), name='home'),
    path('', HomeView.as_view(), name='home'),
    path('orchids/', CultivatedOrchidListView.as_view(), name='orchid_list'),
    path('eventi/', OrchidEventListView.as_view(), name='event_list'),
    path('eventi/nuovo/', OrchidEventCreateView.as_view(), name='event_create'),
]

# API
urlpatterns += [
    path('api/orchidee/genere/', api_orchidee_per_genere, name='api_orchidee_per_genere'),
    ]

# API REST
router = DefaultRouter()
router.register(r'acquisti', OrchidPurchaseViewSet, basename='acquisto')
urlpatterns += [
    path('api/', include(router.urls)),
]
