from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

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