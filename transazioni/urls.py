from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='transazioni'),
    path('nuova_transazione/', views.crea_transazione, name='nuova_transazione'),
    #path('dettaglio/<string:transazione_id>/', views.dettaglio_transazione, name='dettaglio_transazione'),
]