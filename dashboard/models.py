from datetime import datetime

from django.db import models

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class Valuta(models.Model):
    sigla = models.CharField(max_length=3,  null=False, unique=True)
    cambio = models.DecimalField(decimal_places=15, max_digits=30)
    nome = models.CharField(max_length=25)

    class Meta:
        ordering = ('sigla',)

    def __str__(self):
        return self.sigla

    def converti_cambio(self, valuta):
        return float(self.cambio)/float(valuta.cambio)

    @staticmethod
    def crea_valuta(sigla, cambio, nome):
        return Valuta.objects.create(sigla=sigla, cambio=cambio, nome=nome)

class Wallet(models.Model):
    wallet_id = models.CharField(max_length=35, null=False, unique=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    cambio_selezionato = models.ForeignKey(Valuta, on_delete=models.CASCADE)
    transazione_ingresso = models.ManyToManyField('Wallet', null=True, through='Transazione', related_name="transazione_uscita",symmetrical=False)
    ultimo_aggiornamento = models.DateTimeField(default=datetime(1998, 1, 30, 12, 00))

    def __str__(self):
        return self.wallet_id

    def calcola_totale_wallet(self):
        totale = 0
        for conto in self.conti.all():
            totale += conto.calcola_totale_conto(self.cambio_selezionato)
        return totale

    def aggiungi_conto(self, valuta):
        Conto.crea_conto(valuta, self)

    def rimuovi_conto(self, valuta):
        self.conti.get(tipo_valuta=valuta).delete()

    def modifica_cambio_selezionato(self,valuta):
        self.cambio_selezionato = valuta

    def avvia_transazione(self,utente_destinatario,valuta,importo):
        None

    def get_transazioni_uscita(self):
        return self.transazione_uscita.all()

    def get_transazioni_ingresso(self):
        return self.transazione_ingresso.all()

    @staticmethod
    def crea_wallet(wallet_id, user_id, cambio_selezionato):  # metodo statico per la generazione di un nuovo conto
        return Wallet.objects.create(wallet_id=wallet_id, user_id=user_id, cambio_selezionato=cambio_selezionato)

    @staticmethod
    def add_account():  # crea e associa un wallet a un utente
        None

    def delete_account(self):  # cancella il wallet al momento della cancellazione di un utente
        utente = User.objects.get(id=self.user_id.pk)
        # altre validazioni sull'utente...
        utente.delete()
        self.delete()


class Conto(models.Model):
    tipo_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE, default=None)
    importo = models.DecimalField(default=0, decimal_places=15, max_digits=30)
    wallet_associato = models.ForeignKey(Wallet, related_name='conti', on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo_valuta.sigla

    class Meta:
        unique_together = ('tipo_valuta', 'wallet_associato')

    def calcola_totale_conto(self,valuta):  # calcola il totale nella valuta richiesta
        return (float(self.tipo_valuta.cambio)/float(valuta.cambio))*float(self.importo)

    def aggiungi_importo(self,importo):
        self.importo += importo

    def rimuovi_importo(self,importo):
        if (self.importo < importo):
            raise Exception('Il wallet non ha abbastanza fondi')
        else:
            self.importo -= importo

    # probabilmente non verrà utilizzata
    def get_url(self):  # restituisce l'url per l'editing/deleting dell'oggetto
        None

    @staticmethod
    def crea_conto(tipo_valuta, wallet):  # metodo statico per la generazione di un nuovo conto
        return Conto.objects.create(tipo_valuta=tipo_valuta, wallet_associato=wallet)


class Transazione(models.Model):
    id_transazione = models.CharField(max_length=32, null=False, unique=True)
    data = models.DateTimeField(auto_now=True)
    input_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='input_wallet_id')
    output_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='output_wallet_id')
    cryptocurrency = models.ForeignKey(Valuta, on_delete=models.CASCADE)
    quantita = models.DecimalField(decimal_places=15, max_digits=30)

    @staticmethod
    def crea_transazione(wallet_input,wallet_output,tipo_valuta,importo):
        return Transazione.objects.create(id_transazione=get_random_string(length=32),input_wallet=wallet_input, output_wallet=wallet_output, cryptocurrency=tipo_valuta, quantita=importo)

    def get_url(self):  #restituisce l'url dell'istanza della transazione
        None

    def __str__(self):
        return self.id_transazione
