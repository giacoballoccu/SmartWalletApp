from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm



@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


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
            messages.success(request, f'Account creato con successo! Benvenuto {username}!')
            return redirect(dashboard)
    else:
        form = UserRegisterForm()
    return render(request, 'users/registrazione.html', {'form': form})