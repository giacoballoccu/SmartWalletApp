from django.contrib import messages
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
    transazioni_ricevute = Transazione.objects.filter(output_wallet=user_wallet)
    return render(request, 'transazioni.html', {'transazioni_inviate': transazioni_inviate,
                                                'transazioni_ricevute': transazioni_ricevute, })


@login_required
def dettaglio_transazione(request, id):
    transazione = Transazione.objects.get(id=id)
    return render(request, 'dettaglitransazione.html', {'transazione': transazione})


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
            try:
                logged_user_conto = Conto.objects.get(wallet_associato=logged_user_wallet, tipo_valuta=cryptocurrency)
            except Conto.DoesNotExist:
                logged_user_conto = None
            try:
                conto_destinatario = Conto.objects.get(wallet_associato=wallet_destinatario, tipo_valuta=cryptocurrency)
            except Conto.DoesNotExist:
                conto_destinatario = None


            if(logged_user_conto):
                if(logged_user_conto.importo > submitted_form.get("quantita")):
                    logged_user_conto.rimuovi_importo(quantita)
                    logged_user_conto.save()

                    if(conto_destinatario):
                        if (conto_destinatario == logged_user_conto):  # Provvisorio
                            messages.warning(request, 'Non puoi inviarti denaro da solo')
                            return render(request, 'creatransazione.html', {'form': form})
                        conto_destinatario.aggiungi_importo(quantita)
                        conto_destinatario.save()
                    else:
                        newConto = Conto.crea_conto(cryptocurrency,wallet_destinatario)
                        newConto.aggiungi_importo(quantita)
                        newConto.save()

                    nuovaTransazione = Transazione.crea_transazione(logged_user_wallet, wallet_destinatario, cryptocurrency, quantita)
                    nuovaTransazione.save()
                    messages.success(request, 'Transazione effettuata con successo')
                    redirect(index)
                else:
                    messages.warning(request, 'Transazione rifiutata! Non disponi di abbastanza fondi')
                    return render(request, 'creatransazione.html', {'form': form})

            else:
                messages.warning(request, 'Transazione non effettuata! Non possiedi un conto per la moneta selezionata')
                return render(request, 'creatransazione.html', {'form': form})

    else:
        form = TransazioneForm()
    return render(request, 'creatransazione.html', {'form': form})