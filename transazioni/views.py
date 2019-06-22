from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import *

@login_required
def index(request):
    user_wallet = Wallet.objects.get(user_id=request.user)
    transazioni_inviate = Transazione.objects.filter(input_wallet=user_wallet)
    transazioni_ricevute = Transazione.objects.filter(input_wallet=user_wallet)
    return render(request, 'transazioni.html', {'transazioni_inviate': transazioni_inviate,
                                                'transazioni_ricevute': transazioni_ricevute, })


@login_required
def dettaglio_transazione(request):
    return


@login_required
def crea_transazione(request):
    return