from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'transazioni.html')


@login_required
def dettaglio_transazione(request):
    return


@login_required
def crea_transazione(request):
    return