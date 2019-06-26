from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('aggiungi_conto/', views.aggiungi_conto, name='aggiungi_conto'),
    path('rimuovi_conto/(?P<id>\d+)/', views.rimuovi_conto, name='elimina_conto'),
    path('selezione_cambio/', views.modifica_cambio_dashboard, name='selezione_cambio')
]