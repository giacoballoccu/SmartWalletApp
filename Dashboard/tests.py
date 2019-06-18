from django.test import TestCase
from django.contrib.auth.models import User
from .models import Valuta, Conto, Wallet
from django.core.exceptions import *


class ValutaModelTest(TestCase):
    @classmethod
    def SetUpTestData(cls):
        Valuta.objects.create(sigla="USD", cambio="1.0", nome="Dollaro")
        Valuta.objects.create(sigla="BTC", cambio="8000.0", nome="BitCoin")
        Valuta.objects.create(sigla="EUR", cambio="1.2", nome="Euro")

    def test_sigla_testo(self):
        dollaro = Valuta.objects.get(sigla="USD")
        # controlla che sia massimo 3 caratteri
        max_lenght = dollaro._meta.get_field("sigla").max_lenght
        self.assertEqual(max_lenght, 3)
        # controlla che abbia il giusto valore
        self.assertEqual('Dollaro', dollaro._meta.get_field("sigla").verbose_name)

    def test_sigla_unica(self):
        bitcoin = Valuta.objects.get(sigla="BTC")
        self.assertEqual(bitcoin._meta.get_field("sigla").unique, True)

    def test_cambio(self):
        bitcoin = Valuta.objects.get(sigla="BTC")
        self.assertEqual(bitcoin.cambio,8000.0)

    def test_nome_testo(self):
        dollaro = Valuta.objects.get(sigla="USD")
        # controlla che sia massimo 14 caratteri
        max_lenght = dollaro._meta.get_field("nome").max_lenght
        self.assertEqual(max_lenght, 14)
        # controlla che abbia il giusto valore
        self.assertEqual('Dollaro', dollaro.nome)

    def test_conversione_cambio(self):
        dollaro = Valuta.objects.get(sigla="USD")
        bitcoin = Valuta.objects.get(sigla="BTC")
        euro = Valuta.objects.get(sigla="BTC")
        # controlla i tassi convertiti
        self.assertEqual(dollaro.converti_cambio('BTC'), 1.0 / 8000)
        self.assertEqual(euro.converti_cambio('BTC'), 1.2 / 8000)


class WalletModelTest(TestCase):
    @classmethod
    def SetUpTestData(cls):
        Valuta.objects.create(sigla="USD", cambio="1.0", nome="Dollaro")
        Valuta.objects.create(sigla="BTC", cambio="8000.0", nome="BitCoin")
        Valuta.objects.create(sigla="EUR", cambio="1.2", nome="Euro")
        Wallet.crea_utente('Mario', 'RossiMario')
        Wallet.crea_utente('Guido', 'GuidoGuidi')

    def test_creation(self):
        wallet = Wallet.objects.get(user_id=User.objects.get(id=0))
        # controlla la relazione con la valuta di default
        self.assertTrue(wallet._meta.get_field("cambio_selezionato").many_to_one)
        self.assertEqual(wallet._meta.get_field("cambio_selezionato").related_model, Valuta)
        # controlla la valuta selezionata di default
        self.assertEqual(wallet.cambio_selezionato, Valuta.objects.get(sigla="USD"))
        # controlla la relazione con i conti aperti
        self.assertTrue(wallet._meta.get_field("conti").one_to_many)
        self.assertTrue(wallet._meta.get_field("conti").related_model, Conto)
        # controlla che il wallet sia senza conti alla creazione
        self.assertIsNone(wallet.conti.all())

    def test_aggiunta_conto(self):
        wallet = Wallet.objects.get(user_id=User.objects.get(id=0))
        wallet.aggiungi_conto(Valuta.objects.get(sigla="BTC"), 1.0)
        # controlla che il conto sia stato creato
        self.assertEqual(wallet.conti.all().count, 1)
        # controlla che ci sia l'importo nel conto aggiunto
        self.assertEqual(wallet.conti.get(tipoValuta=Valuta.objects.get(sigla="BTC")).importo, 1.0)

    def test_modifica_cambio_selezionato(self):
        wallet = Wallet.objects.get(user_id=User.objects.get(id=0))
        self.assertEqual(wallet.cambio_selezionato, Valuta.objects.get(sigla="USD"))
        wallet.modifica_cambio_selezionato(Valuta.objects.get(sigla="BTC"))
        self.assertEqual(wallet.cambio_selezionato, Valuta.objects.get(sigla="BTC"))

    def test_calcolo_totale_wallet(self):
        wallet = Wallet.objects.get(user_id=User.objects.get(id=0))
        wallet.aggiungi_conto(Valuta.objects.get(sigla="USD"), 8000.0)
        self.assertEqual(wallet.conti.all().count, 2)
        # controllo cambio con il dollaro
        wallet.modifica_cambio_selezionato(Valuta.objects.get(sigla="USD"))
        self.assertEqual(wallet.calcola_totale_wallet(), 16000.0)
        # controllo cambio con il bitcoin
        wallet.modifica_cambio_selezionato(Valuta.objects.get(sigla="BTC"))
        self.assertEqual(wallet.calcola_totale_wallet(), 2.0)

    def test_rimuovi_conto(self):
        wallet = Wallet.objects.get(user_id=User.objects.get(id=0))
        self.assertEqual(wallet.conti.all().count, 2)
        # controllo effettiva rimozione conto
        wallet.rimuovi_conto(Valuta.objects.get(sigla="BTC"))
        self.assertEqual(wallet.conti.all().count, 1)
        # controllo errore se il conto di quella valuta non esiste
        self.assertRaises(ObjectDoesNotExist, wallet.rimuovi_conto(Valuta.objects.get(sigla="BTC")))

class ContoModelTest(TestCase):
    @classmethod
    def SetUpTestData(cls):
        None