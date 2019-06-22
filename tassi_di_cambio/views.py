from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pip._vendor import requests
from django.http import JsonResponse

@login_required
def convertitore(request):
    api = extract_api()
    coins_array = []
    coins_json = sorted(api[:75], key=lambda k: k['data_trade_count'], reverse=True)

    for crypto in coins_json:
        coins_array.append(crypto['asset_id'])

    return render(request, 'convertivalute.html', {'lista': coins_array})


#Metodi utility
def extract_api():
    url = 'https://rest.coinapi.io/v1/assets'
    headers = {'X-CoinAPI-Key': '69F1583F-2188-4BD8-A106-287F3647991E'}
    response = requests.get(url, headers=headers)
    return response.json()


#Ajax

def get_rates(request):
    input_currency = request.GET.get('currency-1')
    output_currency = request.GET.get('currency-2')
    url = 'https://rest.coinapi.io/v1/exchangerate/' + input_currency + '/' + output_currency
    headers = {'X-CoinAPI-Key': '69F1583F-2188-4BD8-A106-287F3647991E'}
    response = requests.get(url, headers=headers)
    coins_and_rates = response.json()

    data = {
        'coin1': coins_and_rates["asset_id_base"], #first currency
        'coin2': coins_and_rates["asset_id_quote"], #second currency
        'rates': coins_and_rates["rate"] #live value

    }

    return JsonResponse(data)