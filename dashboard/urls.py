from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('aggiungi_conto/', views.aggiungi_conto, name='aggiungi_conto'),
    #path('modifica_conto/<string:valuta_type>/', views.modifica_importo, name='modifica_importo_conto'),
    #path('rimuovi_conto/<string:valuta_type>', views.rimuovi_conto, name='rimuovi_conto'),
    #path('selezione_cambio/', views.modifica_cambio_dashboard, nome='selezione_cambio')
]