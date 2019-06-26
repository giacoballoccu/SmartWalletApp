
import decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, NewContoForm
from .models import *
from django.utils.crypto import get_random_string
from pip._vendor import requests

WALLET_ID_NUMBER_OF_CHAR = 32
NUMBER_OF_COINS = 25

@login_required
def dashboard(request):
    user_wallet = Wallet.objects.get(user_id=request.user)
    conti = Conto.objects.filter(wallet_associato=user_wallet).order_by('-tipo_valuta').reverse()
    if(conti):
        totale = conti[0].calcola_totale_conto(user_wallet.cambio_selezionato)
    else:
        totale = 0


    return render(request, 'dashboard.html', {
        'conti': conti,
        'totale': '%.9f'%totale,
        'cambio_selezionato': user_wallet.cambio_selezionato.sigla,
        'ultimo_aggiornamento': user_wallet.ultimo_aggiornamento
    })


@login_required
def aggiungi_conto(request):
    if request.method == 'POST':
        form = NewContoForm(request.POST)
        if form.is_valid():
            submitted_form = form.cleaned_data
            currency = submitted_form.get("tipo_valuta")
            logged_user_wallet = Wallet.objects.get(user_id=request.user.id)
            try:
                logged_user_conto = Conto.objects.get(wallet_associato=logged_user_wallet, tipo_valuta=currency)
            except Conto.DoesNotExist:
                logged_user_conto = None
            if(logged_user_conto):
                messages.error(request, 'Hai già un conto associato a questa moneta!')
                return render(request, 'aggiungiconto.html', {'form': NewContoForm()})
            else:
                newConto = Conto.crea_conto(tipo_valuta=currency, wallet=logged_user_wallet)
                newConto.save()
                messages.success(request, 'Conto creato con successo!')
                redirect(dashboard)
    else:
        form = NewContoForm()
    return render(request, 'aggiungiconto.html', {'form': form})


@login_required
def rimuovi_conto(request):
    return render(request, 'dashboard.html')






@login_required
def modifica_cambio_dashboard(request, tipo_valuta):
    return redirect(dashboard)



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
    return render(request, 'users/registrazione.html', {'form': form, 'title': "Registrati - Smartwallet"})






