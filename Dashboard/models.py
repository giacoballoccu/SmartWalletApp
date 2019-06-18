from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Valuta(models.Model):
    sigla = models.CharField(max_length=5,  null=False, unique=True)
    cambio = models.IntegerField(null=False)
    nome = models.CharField(max_length=25, null=False)

    class Meta:
        ordering = ('sigla',)

    def __unicode__(self):
        None

    def converti_cambio(self,valuta):
        self.cambio = valuta.cambio/self.cambio


class Conto(models.Model):
    tipo_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE, null=False)
    importo = models.IntegerField(default=0)

    def __unicode__(self):
        None

    def calcola_totale_conto(self,valuta):
        None

    def aggiungi_importo(self,importo):
        None

    def rimuovi_importo(self,importo):
        None

    def get_url(self):
        None

    @staticmethod
    def crea_conto(utente,valuta,importo):
        None

    @staticmethod
    def rimuovi_conto(utente, valuta):
        None



class Wallet(models.Model):
    wallet_id = models.CharField(max_length=35, null=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    conti = models.ForeignKey(Conto, on_delete=models.CASCADE)
    cambio_selezionato = models.ForeignKey(Valuta)

    def __unicode__(self):
        None

    def calcola_totale_wallet(self):
        None

    def aggiungi_conto(self,valuta,importo):
        None

    def rimuovi_conto(self,valuta):
        None

    def modifica_cambio_selezionato(self,valuta):
        None

    def avvia_transazione(self,utente_destinatario,valuta,importo):
        None


class Transazione(models.Model):
    id_transazione = models.CharField(max_length=32, null=False, unique=True)
    data = models.DateTimeField(default=timezone.now(), null=False)
    input_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=False)
    output_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=False)
    cryptocurrency = models.CharField(max=5, null=False)
    quantita = models.IntegerField(null=False)


