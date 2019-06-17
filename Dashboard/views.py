from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    #context = {}
    return


@login_required
def aggiungi_conto(request):
    return


@login_required
def rimuovi_conto(request):
    return


@login_required
def modifica_importo(request):
    return


@login_required
def convertitore(request):
    return


@login_required
def modifica_cambio_dashboard(request):
    return
