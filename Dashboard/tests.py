from django.test import TestCase
from django.contrib.auth.models import User
from .models import Valuta, Conto, Wallet
from django.core.exceptions import *


class ValutaModelTest(TestCase):
    def setUp(self):
        self.dollaro = Valuta.objects.create(sigla="USD", cambio="1.0", nome="Dollaro")
        self.bitcoin = Valuta.objects.create(sigla="BTC", cambio="8000.0", nome="Bitcoin")
        self.euro = Valuta.objects.create(sigla="EUR", cambio="1.2", nome="Euro")

    def test_sigla_testo(self):
        # controlla che sia massimo 3 caratteri
        max_lenght = self.dollaro._meta.get_field("sigla").max_length
        self.assertEqual(max_lenght, 3)
        # controlla che abbia il giusto valore
        self.assertEqual('USD', self.dollaro.sigla)

    def test_sigla_unica(self):
        self.assertEqual(self.bitcoin._meta.get_field("sigla").unique, True)

    def test_cambio(self):
        self.assertEqual(float(self.bitcoin.cambio), 8000.0)

    def test_nome_testo(self):
        # controlla che sia massimo 25 caratteri
        max_lenght = self.dollaro._meta.get_field("nome").max_length
        self.assertEqual(max_lenght, 25)
        # controlla che abbia il giusto valore
        self.assertEqual('Dollaro', self.dollaro.nome)

    def test_conversione_cambio(self):
        # controlla i tassi convertiti
        self.assertEqual(self.dollaro.converti_cambio(self.bitcoin), 1.0 / 8000)
        self.assertEqual(self.euro.converti_cambio(self.bitcoin), 1.2 / 8000)


class WalletModelTest(TestCase):

    def setUp(self):
        self.dollaro = Valuta.objects.create(sigla="USD", cambio="1.0", nome="Dollaro")
        self.bitcoin = Valuta.objects.create(sigla="BTC", cambio="8000.0", nome="BitCoin")
        self.euro = Valuta.objects.create(sigla="EUR", cambio="1.2", nome="Euro")
        self.mario = User.objects.create_user(username='mariorossi', password='marioRossi1')
        self.wallet_mario = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.dollaro)

    def test_campo_id(self):
        self.assertEqual(self.wallet_mario._meta.get_field("wallet_id").max_lenght, 35)
        self.assertTrue(self.wallet_mario._meta.get_field("wallet_id").unique)

    def test_campo_user_id(self):
        self.assertTrue(self.wallet_mario._meta.get_field("user_id").one_to_one)
        self.assertEqual(self.wallet_mario._meta.get_field("user_id").related_model, User)

    def test_campo_cambio_selezionato(self):
        self.assertTrue(self.wallet_mario._meta.get_field("cambio_selezionato").many_to_one)
        self.assertEqual(self.wallet_mario._meta.get_field("cambio_selezionato").related_model, Valuta)

    def test_creation(self):
        # controlla la relazione con la valuta di default
        self.assertTrue(self.wallet_mario._meta.get_field("cambio_selezionato").many_to_one)
        self.assertEqual(self.wallet_mario._meta.get_field("cambio_selezionato").related_model, Valuta)
        # controlla la valuta selezionata di default
        self.assertEqual(self.wallet_mario.cambio_selezionato, Valuta.objects.get(sigla="USD"))
        # controlla la relazione con i conti aperti
        self.assertTrue(self.wallet_mario._meta.get_field("conti").one_to_many)
        self.assertTrue(self.wallet_mario._meta.get_field("conti").related_model, Conto)
        # controlla che il self.wallet_mario sia senza conti alla creazione
        self.assertEqual(self.wallet_mario.conti.all().count(), 0)

    def test_aggiunta_conto(self):
        Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=self.wallet_mario)
        # controlla che il conto sia stato creato
        self.assertEqual(self.wallet_mario.conti.all().count(), 1)
        # controlla che ci sia l'importo nel conto aggiunto
        self.assertEqual(self.wallet_mario.conti.get(tipo_valuta=self.bitcoin).importo, 1.0)

    def test_aggiunta_conto_con_funzione(self):
        self.wallet_mario.aggiungi_conto(self.bitcoin, 1.0)
        # controlla che il conto sia stato creato
        self.assertEqual(self.wallet_mario.conti.all().count(), 1)
        # controlla che ci sia l'importo nel conto aggiunto
        self.assertEqual(self.wallet_mario.conti.get(tipo_valuta=self.bitcoin).importo, 1.0)

    def test_aggiunta_conto_di_valuta_uguale_a_esistente(self):
        None

    def test_get_conti(self):
        self.self.wallet_mario.aggiungi_conto(self.bitcoin, 1.0)
        self.assertEqual(self.wallet_mario.conti.importo, 1.0)
        
    def test_modifica_cambio_selezionato(self):
        self.assertEqual(self.wallet_mario.cambio_selezionato, self.dollaro)
        self.wallet_mario.cambio_selezionato = self.bitcoin
        self.assertEqual(self.wallet_mario.cambio_selezionato, self.bitcoin)

    def test_modifica_cambio_selezionato_con_funzione(self):
        self.assertEqual(self.wallet_mario.cambio_selezionato, self.dollaro)
        self.wallet_mario.modifica_cambio_selezionato(self.bitcoin)
        self.assertEqual(self.wallet_mario.cambio_selezionato, self.bitcoin)

    def test_calcolo_totale_wallet(self):
        conto = Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=self.wallet_mario)
        conto = Conto.objects.create(tipo_valuta=self.dollaro, importo=8000.0, wallet_associato=self.wallet_mario)
        self.assertEqual(self.wallet_mario.conti.all().count(), 2)
        # controllo cambio con il dollaro
        self.wallet_mario.cambio_selezionato=self.dollaro
        self.assertEqual(self.wallet_mario.calcola_totale_wallet(), 16000.0)
        # controllo cambio con il bitcoin
        self.wallet_mario.cambio_selezionato = self.bitcoin
        self.assertEqual(self.wallet_mario.calcola_totale_wallet(), 2.0)

    def test_rimuovi_conto(self):
        conto = Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=self.wallet_mario)
        conto = Conto.objects.create(tipo_valuta=self.dollaro, importo=1.0, wallet_associato=self.wallet_mario)
        self.assertEqual(self.wallet_mario.conti.all().count(), 2)
        # controllo effettiva rimozione conto
        # self.wallet_mario.rimuovi_conto(Valuta.objects.get(sigla="BTC"))
        conto.delete()
        self.assertEqual(self.wallet_mario.conti.all().count(), 1)
        # controllo errore se il conto di quella valuta non esiste
        self.assertEqual(0, self.wallet_mario.conti.filter(tipo_valuta=self.dollaro).count())
        
    def test_rimuovi_conto_con_funzione(self):
        conto = Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=self.wallet_mario)
        self.assertEqual(self.wallet_mario.conti.all().count(), 1)
        self.wallet_mario.rimuovi_conto(self.bitcoin)
        self.assertEqual(self.wallet_mario.conti.all().count(), 0)
        None

    def test_rimuovi_conto_che_non_esiste(self):
        None
        
    def test_utente_eliminato_comporta_wallet_eliminato(self):
        None

    def test_get_lista_transazioni(self):
        None


class ContoModelTest(TestCase):
    @classmethod
    def SetUpTestData(cls):
        None