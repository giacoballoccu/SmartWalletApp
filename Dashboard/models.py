from django.db import models


class Valuta(models.Model):
    sigla = None
    cambio = None
    nome = None

    def __unicode__(self):
        None

    def converti_cambio(self,valuta):
        None


class Conto(models.Model):
    tipo_valuta = None
    importo = None
    # id = None
    # wallet_id = None

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
    id = None
    user_id = None
    conti = None
    cambio_selezionato = None

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
