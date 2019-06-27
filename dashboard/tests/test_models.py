from django.test import TestCase
from django.contrib.auth.models import User
from dashboard.models import Valuta, Conto, Wallet
from django.core.exceptions import *


class WalletModelTest(TestCase):

    def setUp(self):
        self.dollaro = Valuta.objects.create(sigla="USD", cambio="1.0", nome="Dollaro")
        self.bitcoin = Valuta.objects.create(sigla="BTC", cambio="8000.0", nome="BitCoin")
        self.euro = Valuta.objects.create(sigla="EUR", cambio="1.2", nome="Euro")
        self.mario = User.objects.create_user(username='mariorossi', password='marioRossi1')
        self.wallet_mario = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.dollaro)

    def test_field_wallet_id(self):
        self.assertEqual(self.wallet_mario._meta.get_field("wallet_id").max_length, 35)
        self.assertTrue(self.wallet_mario._meta.get_field("wallet_id").unique)

    def test_field_user_id(self):
        self.assertTrue(self.wallet_mario._meta.get_field("user_id").one_to_one)
        self.assertEqual(self.wallet_mario._meta.get_field("user_id").related_model, User)

    def test_campo_cambio_selezionato(self):
        self.assertTrue(self.wallet_mario._meta.get_field("cambio_selezionato").many_to_one)
        self.assertEqual(self.wallet_mario._meta.get_field("cambio_selezionato").related_model, Valuta)

    def test_creation(self):
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
        self.wallet_mario.aggiungi_conto(self.bitcoin)
        # controlla che il conto sia stato creato
        self.assertEqual(self.wallet_mario.conti.all().count(), 1)
        # controlla che ci sia l'importo nel conto aggiunto
        self.assertEqual(self.wallet_mario.conti.get(tipo_valuta=self.bitcoin).importo, 0)

    def test_get_conti(self):
        self.wallet_mario.aggiungi_conto(self.bitcoin)
        self.assertEqual(self.wallet_mario.conti.get(tipo_valuta=self.bitcoin).importo)
        
    def test_modifica_cambio_selezionato(self):
        self.assertEqual(self.wallet_mario.cambio_selezionato, self.dollaro)
        self.wallet_mario.cambio_selezionato = self.bitcoin
        self.assertEqual(self.wallet_mario.cambio_selezionato, self.bitcoin)

    def test_modifica_cambio_selezionato_con_funzione(self):
        self.assertEqual(self.wallet_mario.cambio_selezionato, self.dollaro)
        self.wallet_mario.modifica_cambio_selezionato(self.bitcoin)
        self.assertEqual(self.wallet_mario.cambio_selezionato, self.bitcoin)

    def test_calcolo_totale_wallet(self):
        Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=self.wallet_mario)
        Conto.objects.create(tipo_valuta=self.dollaro, importo=8000.0, wallet_associato=self.wallet_mario)
        self.assertEqual(self.wallet_mario.conti.all().count(), 2)
        # controllo cambio con il dollaro
        self.wallet_mario.cambio_selezionato=self.dollaro
        self.assertEqual(self.wallet_mario.calcola_totale_wallet(), 16000.0)
        # controllo cambio con il bitcoin
        self.wallet_mario.cambio_selezionato = self.bitcoin
        self.assertEqual(self.wallet_mario.calcola_totale_wallet(), 2.0)

    def test_rimuovi_conto(self):
        Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=self.wallet_mario)
        conto = Conto.objects.create(tipo_valuta=self.dollaro, importo=1.0, wallet_associato=self.wallet_mario)
        self.assertEqual(self.wallet_mario.conti.all().count(), 2)
        # controllo effettiva rimozione conto
        conto.delete()
        self.assertEqual(self.wallet_mario.conti.all().count(), 1)
        # controllo errore se il conto di quella valuta non esiste
        self.assertEqual(0, self.wallet_mario.conti.filter(tipo_valuta=self.dollaro).count())
        
    def test_rimuovi_conto_con_funzione(self):
        Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=self.wallet_mario)
        self.assertEqual(self.wallet_mario.conti.all().count(), 1)
        self.wallet_mario.rimuovi_conto(self.bitcoin)
        self.assertEqual(self.wallet_mario.conti.all().count(), 0)

    def test_rimuovi_conto_che_non_esiste(self):
        Conto.objects.create(tipo_valuta=self.bitcoin, importo=0.0, wallet_associato=self.wallet_mario)
        self.assertEqual(self.wallet_mario.conti.all().count(), 1)
        # controllo che ci sia un eccezione
        self.assertRaises(Exception, lambda: self.wallet_mario.rimuovi_conto(self.dollaro))
        self.assertEqual(self.wallet_mario.conti.all().count(), 1)
        
    def test_utente_eliminato_comporta_wallet_eliminato(self):
        self.wallet_mario.delete_account()
        self.assertEqual(self.wallet_mario.wallet_id, '')
        self.assertEqual(Wallet.objects.all().count(), 0)

    def test_get_lista_transazioni(self):
        None


class ContoModelTest(TestCase):
    def setUp(self):
        self.dollaro = Valuta.objects.create(sigla="USD", cambio="1.0", nome="Dollaro")
        self.bitcoin = Valuta.objects.create(sigla="BTC", cambio="8000.0", nome="BitCoin")
        self.euro = Valuta.objects.create(sigla="EUR", cambio="1.2", nome="Euro")
        self.mario = User.objects.create_user(username='mariorossi', password='marioRossi1')
        self.wallet_mario = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.dollaro)
        self.conto = Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=self.wallet_mario)

    def test_field_tipo_valuta(self):
        self.assertTrue(self.conto._meta.get_field('tipo_valuta').many_to_one)
        self.assertEqual(self.conto._meta.get_field('tipo_valuta').related_model, Valuta)

    def test_field_wallet_associato(self):
        self.assertTrue(self.conto._meta.get_field('wallet_associato').many_to_one)
        self.assertEqual(self.conto._meta.get_field('wallet_associato').related_model, Wallet)

    def test_field_importo(self):
        self.assertTrue(self.conto._meta.get_field('importo').max_digits, 30)

    def test_creazione(self):
        self.assertEqual(self.conto.wallet_associato, self.wallet_mario)
        self.assertEqual(self.conto.tipo_valuta, self.bitcoin)
        self.assertEqual(self.conto.importo, 1)

    def test_creazione_con_funzione(self):
        conto = Conto.crea_conto(self.euro, self.wallet_mario)
        self.assertEqual(conto.tipo_valuta, self.euro)
        self.assertEqual(conto.wallet_associato, self.wallet_mario)
        self.assertEqual(conto.importo, 0)

    def test_creazione_conto_di_tipo_esistente(self):
        self.assertRaises(Exception, lambda: Conto.crea_conto(self.bitcoin, 1.0, self.wallet_mario))

    def test_calcolo_totale_conto(self):
        self.assertEqual(self.conto.calcola_totale_conto(self.conto.tipo_valuta), 1.0)
        self.assertEqual(self.conto.calcola_totale_conto(self.dollaro), 8000.0)

    def test_aggiunta_importo(self):
        self.conto.aggiungi_importo(1.0)
        self.assertEqual(self.conto.importo, 2.0)

    def test_rimozione_importo(self):
        self.conto.rimuovi_importo(0.3)
        self.assertEqual(self.conto.importo, 0.7)

    def test_rimozione_importo_da_conto_senza_copertura(self):
        self.assertRaises(Exception, lambda: self.conto.rimuovi_importo(2.0))
