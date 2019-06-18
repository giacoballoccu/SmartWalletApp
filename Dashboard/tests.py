from django.test import TestCase
from django.contrib.auth.models import User
from .models import Valuta, Conto, Wallet
from django.core.exceptions import *


class ValutaModelTest(TestCase):
    def setUp(self):
        dollaro = Valuta.objects.create(sigla="USD", cambio="1.0", nome="Dollaro")
        bitcoin = Valuta.objects.create(sigla="BTC", cambio="8000.0", nome="Bitcoin")
        euro = Valuta.objects.create(sigla="EUR", cambio="1.2", nome="Euro")

    def test_sigla_testo(self):
        dollaro = Valuta.objects.get(sigla="USD")
        # controlla che sia massimo 3 caratteri
        max_lenght = dollaro._meta.get_field("sigla").max_length
        self.assertEqual(max_lenght, 3)
        # controlla che abbia il giusto valore
        self.assertEqual('USD', dollaro.sigla)

    def test_sigla_unica(self):
        bitcoin = Valuta.objects.get(sigla="BTC")
        self.assertEqual(bitcoin._meta.get_field("sigla").unique, True)

    def test_cambio(self):
        bitcoin = Valuta.objects.get(sigla="BTC")
        self.assertEqual(bitcoin.cambio, 8000.0)

    def test_nome_testo(self):
        dollaro = Valuta.objects.get(sigla="USD")
        # controlla che sia massimo 25 caratteri
        max_lenght = dollaro._meta.get_field("nome").max_length
        self.assertEqual(max_lenght, 25)
        # controlla che abbia il giusto valore
        self.assertEqual('Dollaro', dollaro.nome)

    def test_conversione_cambio(self):
        dollaro = Valuta.objects.get(sigla="USD")
        bitcoin = Valuta.objects.get(sigla="BTC")
        euro = Valuta.objects.get(sigla="EUR")
        # controlla i tassi convertiti
        self.assertEqual(dollaro.converti_cambio(bitcoin), 1.0 / 8000)
        self.assertEqual(euro.converti_cambio(bitcoin), 1.2 / 8000)


class WalletModelTest(TestCase):

    def setUp(self):
        self.dollaro = Valuta.objects.create(sigla="USD", cambio="1.0", nome="Dollaro")
        self.bitcoin = Valuta.objects.create(sigla="BTC", cambio="8000.0", nome="BitCoin")
        self.euro = Valuta.objects.create(sigla="EUR", cambio="1.2", nome="Euro")
        self.mario = User.objects.create_user(username='mariorossi', password='marioRossi1')

    def test_creation(self):
        wallet = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.dollaro)
        # controlla la relazione con la valuta di default
        self.assertTrue(wallet._meta.get_field("cambio_selezionato").many_to_one)
        self.assertEqual(wallet._meta.get_field("cambio_selezionato").related_model, Valuta)
        # controlla la valuta selezionata di default
        self.assertEqual(wallet.cambio_selezionato, Valuta.objects.get(sigla="USD"))
        # controlla la relazione con i conti aperti
        self.assertTrue(wallet._meta.get_field("conti").one_to_many)
        self.assertTrue(wallet._meta.get_field("conti").related_model, Conto)
        # controlla che il wallet sia senza conti alla creazione
        self.assertEqual(wallet.conti.all().count(), 0)

    def test_aggiunta_conto(self):
        wallet_mario = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.dollaro)
        conto = Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=wallet_mario)
        wallet_mario.conti.add(conto)
        # controlla che il conto sia stato creato
        self.assertEqual(wallet_mario.conti.all().count(), 1)
        # controlla che ci sia l'importo nel conto aggiunto
        self.assertEqual(wallet_mario.conti.get(tipo_valuta=self.bitcoin).importo, 1.0)

    def test_get_conto_funzione(self):
        None

    def test_aggiunta_conto_con_funzione(self):
        wallet_mario = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.dollaro)
        wallet_mario.aggiungi_conto(self.bitcoin, 1.0)
        # controlla che il conto sia stato creato
        self.assertEqual(wallet_mario.conti.all().count(), 1)
        # controlla che ci sia l'importo nel conto aggiunto
        self.assertEqual(wallet_mario.conti.get(tipo_valuta=self.bitcoin).importo, 1.0)

    def test_modifica_cambio_selezionato(self):
        wallet_mario = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.dollaro)
        self.assertEqual(wallet_mario.cambio_selezionato, self.dollaro)
        wallet_mario.cambio_selezionato = self.bitcoin
        self.assertEqual(wallet_mario.cambio_selezionato, self.bitcoin)

    def test_modifica_cambio_selezionato_con_funzione(self):
        wallet_mario = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.dollaro)
        self.assertEqual(wallet_mario.cambio_selezionato, self.dollaro)
        wallet_mario.modifica_cambio_selezionato(self.bitcoin)
        self.assertEqual(wallet_mario.cambio_selezionato, self.bitcoin)

    def test_calcolo_totale_wallet(self):
        wallet_mario = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.dollaro)
        conto = Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=wallet_mario)
        conto = Conto.objects.create(tipo_valuta=self.dollaro, importo=8000.0, wallet_associato=wallet_mario)
        self.assertEqual(wallet_mario.conti.all().count(), 2)
        # controllo cambio con il dollaro
        wallet_mario.cambio_selezionato=self.dollaro
        self.assertEqual(wallet_mario.calcola_totale_wallet(), 16000.0)
        # controllo cambio con il bitcoin
        wallet_mario.cambio_selezionato = self.bitcoin
        self.assertEqual(wallet_mario.calcola_totale_wallet(), 2.0)

    def test_rimuovi_conto(self):
        wallet_mario = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.dollaro)
        conto = Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=wallet_mario)
        conto = Conto.objects.create(tipo_valuta=self.dollaro, importo=1.0, wallet_associato=wallet_mario)
        self.assertEqual(wallet_mario.conti.all().count(), 2)
        # controllo effettiva rimozione conto
        # wallet_mario.rimuovi_conto(Valuta.objects.get(sigla="BTC"))
        conto.delete()
        self.assertEqual(wallet_mario.conti.all().count(), 1)
        # controllo errore se il conto di quella valuta non esiste
        self.assertEqual(0, wallet_mario.conti.filter(tipo_valuta=self.dollaro).count())

    def test_get_lista_transazioni(self):
        None

    

class ContoModelTest(TestCase):
    @classmethod
    def SetUpTestData(cls):
        None