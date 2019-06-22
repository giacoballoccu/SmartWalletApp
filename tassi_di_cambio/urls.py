from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.convertitore, name='converti_valute'),
    path('ajax/get_rates/', views.get_rates, name='get_rates'),
]