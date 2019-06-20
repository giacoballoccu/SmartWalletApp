from django.test import TestCase
from django.contrib.auth.models import User
from Dashboard.models import Valuta, Conto, Wallet, Transazione
class TransazioniModelTest(TestCase):
    def setUp(self):
        self.dollaro = Valuta.objects.create(sigla="USD", cambio="1.0", nome="Dollaro")
        self.bitcoin = Valuta.objects.create(sigla="BTC", cambio="8000.0", nome="BitCoin")
        self.euro = Valuta.objects.create(sigla="EUR", cambio="1.2", nome="Euro")
        self.mario = User.objects.create_user(username='mariorossi', password='marioRossi1')
        self.wallet_mario = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.dollaro, wallet_id="abcuno")
        self.conto_mario_bitcoin = Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=self.wallet_mario)
        self.luigi = User.objects.create_user(username='luigialfonsi', password='luigiAlfonsi1')
        self.wallet_luigi = Wallet.objects.create(user_id=self.luigi, cambio_selezionato=self.dollaro,wallet_id="abcdue")
        self.conto_luigi_bitcoin = Conto.objects.create(tipo_valuta=self.bitcoin, importo=1.0, wallet_associato=self.wallet_luigi)
        self.transazione = Transazione.objects.create(
            input_wallet=self.wallet_mario, output_wallet=self.wallet_luigi, valuta=self.bitcoin, quantita=0.5, id_transazione="n2ovF5RE0bc3EwDF6i")

    def test_field_id_transazione(self):
        self.assertEqual(self.transazione._meta.get_field('id_transazione').max_length, 32)

    def test_field_data(self):
        self.assertTrue(self.transazione._meta.get_field('data').auto_now_add)
        self.assertFalse(self.transazione._meta.get_field('data').editable)
        self.assertTrue(self.transazione._meta.get_field('data').blank)

    def test_field_input_wallet(self):
        self.assertTrue(self.transazione._meta.get_field('input_wallet').many_to_one)
        self.assertEqual(self.transazione._meta.get_field('input_wallet').related_model, Wallet)

    def test_field_output_wallet(self):
        self.assertTrue(self.transazione._meta.get_field('output_wallet').many_to_one)
        self.assertEqual(self.transazione._meta.get_field('output_wallet').related_model, Wallet)

    def test_field_valuta(self):
        self.assertTrue(self.transazione._meta.get_field('valuta').many_to_one)
        self.assertEqual(self.transazione._meta.get_field('valuta').related_model, Valuta)

    def test_field_quantita(self):
        self.assertEqual(self.transazione._meta.get_field('quantita').max_digits, 30)

    def test_field_causale(self):
        self.assertEqual(self.transazione._meta.get_field('causale').max_lenght, 45)

    def test_creazione(self):  # la creazione di una riga della tabella non comporta la modifica degli importi dei conti
        self.assertEqual(self.transazione.input_wallet, self.wallet_mario)
        self.assertEqual(self.transazione.output_wallet, self.wallet_luigi)
        self.assertEqual(self.transazione.quantita, 0.5)

    def test_creazione_con_funzione(self):  # in caso è possibile ,crea la transazione
        temp = Transazione.crea_transazione(self.wallet_luigi, self.wallet_mario, self.bitcoin, 0.3)
        self.assertEqual(temp.input_wallet, self.wallet_luigi)
        self.assertEqual(temp.output_wallet, self.wallet_mario)
        self.assertEqual(temp.quantita, 0.3)

        self.assertEqual(self.conto_luigi_bitcoin.importo, 0.7)
        self.assertEqual(self.conto_luigi_bitcoin.importo, 1.3)

    def test_creazione_con_wallet_senza_conto_richiesto(self):
        self.assertRaises(
            Exception, Transazione.crea_transazione(self.wallet_luigi, self.wallet_mario, self.dollaro, 0.3))

    def test_creazione_con_wallet_con_saldo_insufficiente(self):
        self.assertRaises(
            Exception, Transazione.crea_transazione(self.wallet_luigi, self.wallet_mario, self.bitcoin, 1.3))

    def test_creazione_verso_se_stesso(self):
        self.assertRaises(
            Exception, Transazione.crea_transazione(self.wallet_luigi, self.wallet_luigi, self.bitcoin, 0.3))

    def test_get_url(self):
        None