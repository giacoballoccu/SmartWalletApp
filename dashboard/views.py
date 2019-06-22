import decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from .models import *
from django.utils.crypto import get_random_string
from pip._vendor import requests


@login_required
def dashboard(request):
    user_wallet = Wallet.objects.get(user_id=request.user)
    conti = Conto.objects.filter(wallet_associato=user_wallet)
    totale = 0
    for conto in conti:
        totale += conto.importo * get_rate_selected('BTC' , user_wallet.cambio_selezionato.sigla)
    return render(request, 'dashboard.html', {
        'conti': conti,
        'totale': '%.5f'%totale,
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
def get_rate_selected(coin1,coin2):
    url = 'https://rest.coinapi.io/v1/exchangerate/' + coin1 + '/' + coin2
    headers = {'X-CoinAPI-Key': '69F1583F-2188-4BD8-A106-287F3647991E'}
    response = requests.get(url, headers=headers)
    coins_and_rates = response.json()
    return decimal.Decimal(coins_and_rates["rate"])

#Security
def registrazione(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            newWallet = Wallet.crea_wallet(get_random_string(length=32), User.objects.get(username=username), Valuta.objects.get(sigla='USD'))
            newWallet.save()
            messages.success(request, 'Account creato con successo! Benvenuto {username}!')
            return redirect(dashboard)
    else:
        form = UserRegisterForm()
    return render(request, 'users/registrazione.html', {'form': form})






