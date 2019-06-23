
import decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from .models import *
from django.utils.crypto import get_random_string
from pip._vendor import requests

WALLET_ID_NUMBER_OF_CHAR = 32
NUMBER_OF_COINS = 25

@login_required
def dashboard(request):
    user_wallet = Wallet.objects.get(user_id=request.user)
    conti = Conto.objects.filter(wallet_associato=user_wallet)
    if(conti):
        totale = conti[0].calcola_totale_conto(user_wallet.cambio_selezionato)
    else:
        totale = 0


    return render(request, 'dashboard.html', {
        'conti': conti,
        'totale': '%.9f'%totale,
        'ultimo_aggiornamento': user_wallet.ultimo_aggiornamento
    })


@login_required
def aggiungi_conto(request):
    return render(request, 'aggiungiconto.html')


@login_required
def rimuovi_conto(request):
    return render(request, 'dashboard.html')


@login_required
def modifica_importo(request):
    return render(request, 'modificaconto.html')



@login_required
def modifica_cambio_dashboard(request, tipo_valuta):
    return redirect(dashboard)

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

def aggiorna_coin_rates():
    valute = Valuta.objects.all()
    for valuta in valute:
        valuta.cambio = get_rate_dollar(valuta.sigla)
        valuta.save(update_fields=["cambio"])


def get_rate_dollar(coin1):
    if(coin1 == "USD"):
        return 1.0
    else:
        url = 'https://rest.coinapi.io/v1/exchangerate/' + coin1 + '/' + 'USD'
        headers = {'X-CoinAPI-Key': '69F1583F-2188-4BD8-A106-287F3647991E'}
        response = requests.get(url, headers=headers)
        coins_and_rates = response.json()
        return '%.9f'%decimal.Decimal(coins_and_rates['rate'])

#Security
def registrazione(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            newWallet = Wallet.crea_wallet(get_random_string(length=WALLET_ID_NUMBER_OF_CHAR), User.objects.get(username=username), Valuta.objects.get(sigla='USD'))
            newWallet.save()

            messages.success(request, 'Account creato con successo! Benvenuto {username}!')
            return redirect(dashboard)
    else:
        form = UserRegisterForm()
    return render(request, 'users/registrazione.html', {'form': form})






