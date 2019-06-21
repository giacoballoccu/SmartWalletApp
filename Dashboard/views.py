from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from .models import *
from django.utils.crypto import get_random_string



@login_required
def dashboard(request):
    user_wallet = Wallet.objects.get(user_id=request.user)
    conti = Conto.objects.filter(wallet_associato=user_wallet)
    totale = conti[0].calcola_totale_conto(user_wallet.cambio_selezionato)
    return render(request, 'dashboard.html', {
        'conti': conti,
        'totale': totale,
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
def convertitore(request):
    return render(request, 'convertivalute.html')


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
            newWallet = Wallet.crea_wallet(get_random_string(length=32), User.objects.get(username=username), Valuta.objects.get(sigla='USD'))
            newWallet.save()
            messages.success(request, 'Account creato con successo! Benvenuto {username}!')
            return redirect(dashboard)
    else:
        form = UserRegisterForm()
    return render(request, 'users/registrazione.html', {'form': form})

#Metodi utility

