from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

from dashboard.models import *
from dashboard.views import dashboard
from transazioni import forms
from transazioni.forms import TransazioneForm


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
    if request.method == 'POST':
        form = TransazioneForm(request.POST)
        if form.is_valid():
            submitted_form = form.cleaned_data
            wallet_destinatario = submitted_form.get("output_wallet")
            cryptocurrency = submitted_form.get("cryptocurrency")
            quantita = submitted_form.get("quantita")

            logged_user_wallet = Wallet.objects.get(user_id=request.user.id)
            logged_user_conto = Conto.objects.get(wallet_associato=logged_user_wallet, tipo_valuta=cryptocurrency)
            conto_destinatario = Conto.objects.get(wallet_associato=wallet_destinatario, tipo_valuta=cryptocurrency)

            if(logged_user_conto):
                if(logged_user_conto.importo > submitted_form.get("quantita")):
                    logged_user_conto.rimuovi_importo(quantita)
                    logged_user_conto.update()

                    if(conto_destinatario):
                        conto_destinatario.aggiungi_importo(quantita)
                        conto_destinatario.update()
                    else:
                        if(conto_destinatario == logged_user_conto): #Provvisorio
                            messages.error(request, 'Non puoi inviarti denaro da solo')
                            redirect(crea_transazione, form())

                        newConto = Conto.crea_conto(tipo_valuta=cryptocurrency, wallet=wallet_destinatario)
                        newConto.aggiungi_importo(quantita)
                        newConto.save()

                    nuovaTransazione = Transazione.crea_transazione(logged_user_wallet, wallet_destinatario, cryptocurrency, quantita)
                    nuovaTransazione.save()
                    messages.success(request, 'Transazione effettuata con successo')
                    redirect(index)
                else:
                    messages.error(request, 'Transazione rifiutata! Non disponi di abbastanza fondi')
                    redirect(crea_transazione, form())
            else:
                messages.error(request, 'Transazione non effettuata! Non possiedi un conto per la moneta selezionata')
                redirect(crea_transazione, form())
    else:
        form = TransazioneForm()
    return render(request, 'creatransazione.html', {'form': form})






