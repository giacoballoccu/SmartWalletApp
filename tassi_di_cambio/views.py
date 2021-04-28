from datetime import datetime

import decimal
from json import dump

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse

from dashboard.models import Valuta, Wallet
from dashboard.views import NUMBER_OF_COINS


@login_required
def convertitore(request):
    coins_array = list(Valuta.objects.values_list('sigla', flat=True))
    return render(request, 'convertivalute.html', {'lista': coins_array,
                                                   'ultimo_aggiornamento': Wallet.objects.get(user_id=request.user).ultimo_aggiornamento
                                                   })


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

#Ajax
def aggiorna_coin_rates(request):
    user_wallet = Wallet.objects.get(user_id=request.user)
    data_ultimo_aggiornamento = user_wallet.ultimo_aggiornamento
    tempo_trascorso =  datetime.now().replace(tzinfo=None) - data_ultimo_aggiornamento.replace(tzinfo=None)
    tempo_trascorso_giorni = divmod(tempo_trascorso.total_seconds(), 86400)[0]
    if( tempo_trascorso_giorni < 1):
        response = JsonResponse({"error": "Puoi aggiornare le valute solo una volta al giorno"})
        response.status_code = 403
        return response
    else:
        valute = Valuta.objects.all()
        for valuta in valute:
            valuta.cambio = get_rate_dollar(valuta.sigla)
            valuta.save(update_fields=["cambio"])
        user_wallet.ultimo_aggiornamento = datetime.now()
        user_wallet.save(update_fields=["ultimo_aggiornamento"])
        response = JsonResponse({"message": "Cambi aggiornati con successo",
                             'ultimo_aggiornamento': data_ultimo_aggiornamento})
        response.status_code = 200
        return response


#Utility

#Questo metodo è stato utilizzato per inizializzare il db delle valute
def inizializza_valute():
    url = 'https://rest.coinapi.io/v1/assets'
    headers = {'X-CoinAPI-Key': '73034021-0EBC-493D-8A00-E0F138111F41'}
    response = requests.get(url, headers=headers)
    assets_list = sorted(response.json()[:NUMBER_OF_COINS], key=lambda k: k['data_trade_count'], reverse=True)
    for coin in assets_list:
        newValuta = Valuta.crea_valuta(coin['asset_id'], get_rate_dollar(coin['asset_id']), coin['name'])
        newValuta.save()





def get_rate_dollar(coin1):
    if(coin1 == "USD"):
        return 1.0
    else:
        url = 'https://rest.coinapi.io/v1/exchangerate/' + coin1 + '/' + 'USD'
        headers = {'X-CoinAPI-Key': '69F1583F-2188-4BD8-A106-287F3647991E'}
        response = requests.get(url, headers=headers)
        coins_and_rates = response.json()
        return '%.9f'%decimal.Decimal(coins_and_rates['rate'])