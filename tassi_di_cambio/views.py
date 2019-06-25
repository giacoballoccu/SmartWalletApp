from json import dump

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pip._vendor import requests
from django.http import JsonResponse

from dashboard.models import Valuta


@login_required
def convertitore(request):
    coins_array = list(Valuta.objects.values_list('sigla', flat=True))
    return render(request, 'convertivalute.html', {'lista': coins_array})


#Metodi utility
def extract_api():
    url = 'https://rest.coinapi.io/v1/assets'
    headers = {'X-CoinAPI-Key': '69F1583F-2188-4BD8-A106-287F3647991E'}
    response = requests.get(url, headers=headers)
    return response.json()


#Ajax

def get_rates(request):
    currency1 = Valuta.objects.get(sigla=request.GET.get('currency-1'))
    currency2 = Valuta.objects.get(sigla=request.GET.get('currency-2'))
    rate = Valuta.converti_cambio(currency1, currency2)

    data = {
        'coin1': currency1.sigla, #first currency
        'coin2': currency2.sigla, #second currency
        'rates': rate #live value

    }

    return JsonResponse(data)