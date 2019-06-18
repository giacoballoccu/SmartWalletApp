from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User



class Valuta(models.Model):
    sigla = models.CharField(max_length=5,  null=False, unique=True)
    cambio = models.DecimalField(decimal_places=15, max_digits=30)
    nome = models.CharField(max_length=25)

    class Meta:
        ordering = ('sigla',)

    def __str__(self):
        return self.sigla

    def converti_cambio(self,valuta):
        self.cambio = valuta.cambio/self.cambio




class Conto(models.Model):
    tipo_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE, default=None)
    importo = models.DecimalField(default=0,decimal_places=15, max_digits=30)
    wallet_associato = models.ManyToManyField('Wallet')

    class Meta:
        unique_together = (("wallet_associato", "tipo_valuta"),)

    def __str__(self):
        return self.tipo_valuta.sigla

    def __init__(self, tipo_valuta, importo, wallet_associato):
        self.tipo_valuta = tipo_valuta
        self.importo = importo
        self.wallet_associato = wallet_associato

    def calcola_totale_conto(self,valuta):
        None

    def aggiungi_importo(self,importo):
        None

    def rimuovi_importo(self,importo):
        None

    def get_url(self): #?
        None

    @staticmethod
    def crea_conto(utente,valuta,importo):
        None

    @staticmethod
    def rimuovi_conto(utente, valuta):
        None




    @staticmethod
    def crea_utente(username,password):
        None

class Wallet(models.Model):
    wallet_id = models.CharField(max_length=35, null=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    conti = models.ManyToManyField(Conto, related_name='conti')
    cambio_selezionato = models.ForeignKey(Valuta, on_delete=models.CASCADE)

    def __str__(self):
        return self.wallet_id

    def get_conti(self):
        self.conti.all()

    #USD
    def calcola_totale_wallet(self):
        totale = 0
        for conto in self.conti.all():
            totale += conto.importo * conto.tipo_valuta.cambio

        return totale * self.cambio_selezionato

    def aggiungi_conto(self,valuta,importo):
        self.conti.add(Conto(valuta, importo, self.wallet_id))

    def rimuovi_conto(self,valuta):
        self.conti.remove(self.conti.filter(tipo_valuta=valuta, wallet_associato=self.wallet_id))

    def modifica_cambio_selezionato(self,valuta):
        self.cambio_selezionato = valuta

    def avvia_transazione(self,utente_destinatario,valuta,importo):
        None

class Transazione(models.Model):
    id_transazione = models.CharField(max_length=32, null=False, unique=True)
    data = models.DateTimeField(auto_now=True)
    input_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=False, related_name='input_wallet_id')
    output_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=False, related_name='output_wallet_id')
    cryptocurrency = models.ForeignKey(Valuta, on_delete=models.CASCADE)
    quantita = models.DecimalField(decimal_places=15, max_digits=30)


    def __str__(self):
        return self.id_transazione