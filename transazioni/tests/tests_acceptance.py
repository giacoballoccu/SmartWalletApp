from django.test import TestCase
from django.urls import reverse
from dashboard.models import *
from transazioni.models import Transazione

class UtenteAccedeAllaSezioneTransazioni(TestCase):
    def setUp(self):
        self.BTC = Valuta.objects.create(codice='BTC', cambio=8000, nome='Bitcoin')
        self.USD = Valuta.objects.create(codice='USD', cambio=1, nome='Dollaro')
        self.mario = User.objects.create_user(username='mariorossi', password='MarioRossi00')
        self.luigi = User.objects.create_user(username='luigibiasi', password='LuigiBiasi01')
        self.mario_wallet = Wallet.objects.create(user_id=self.mario, valuta_predefinita=self.USD)
        self.luigi_wallet = Wallet.objects.create(user_id=self.luigi, valuta_predefinita=self.USD)
        self.conto_btc_mario = Conto.objects.create(wallet_id=self.mario_wallet, quantita=1.0, valuta=self.BTC)
        self.conto_usd_mario = Conto.objects.create(wallet_id=self.mario_wallet, quantita=0.0, valuta=self.USD)
        self.conto_btc_luigi = Conto.objects.create(wallet_id=self.luigi_wallet, quantita=0.0, valuta=self.BTC)
        self.transazione = Transazione.objects.create(id_transazione='asfbsdaibuieb21',data=time.now(),input_wallet=self.mario_wallet,output_wallet=self.wal)

    def test_get_page_logged_user(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('transazioni'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transazioni.html')
        self.assertEqual(response.context['user'], self.mario)

    def test_get_page_unlogged_user(self):
        response = self.client.get(reverse('transazioni'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'login.html')

    def test_transazioni_list(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('transazioni'))
        self.assertEqual(response.context['transazioni'].length, 1)
        self.assertContains(response.context['transazioni'], self.transazione)

class UtenteCheCreaUnaTransazione(TestCase):
    def setUp(self):
        self.BTC = Valuta.objects.create(codice='BTC', cambio=8000, nome='Bitcoin')
        self.USD = Valuta.objects.create(codice='USD', cambio=1, nome='Dollaro')
        self.mario = User.objects.create_user(username='mariorossi', password='MarioRossi00')
        self.luigi = User.objects.create_user(username='luigibiasi', password='LuigiBiasi01')
        self.mario_wallet = Wallet.objects.create(user_id=self.mario, valuta_predefinita=self.USD)
        self.luigi_wallet = Wallet.objects.create(user_id=self.luigi, valuta_predefinita=self.USD)
        self.conto_btc_mario = Conto.objects.create(wallet_id=self.mario_wallet, quantita=1.0, valuta=self.BTC)
        self.conto_usd_mario = Conto.objects.create(wallet_id=self.mario_wallet, quantita=0.0, valuta=self.USD)
        self.conto_btc_luigi = Conto.objects.create(wallet_id=self.luigi_wallet, quantita=0.0, valuta=self.BTC)
        self.transazione = Transazione.objects.create(id_transazione='asfbsdaibuieb21', data=time.now(),
                                                      input_wallet=self.mario_wallet, output_wallet=self.wal)

    def test_get_page_logged_user(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('nuova_transazione'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nuova_transazione.html')
        self.assertEqual(response.context['user'], self.mario)
        self.assertEqual(response.context['form'],NuovaTransazioneForm)

    def test_get_page_unlogged_user(self):
        response = self.client.get(reverse('nuova_transazione'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'login.html')

    def test_nuova_transazione(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        post_data= NuovaTransazioneForm()
        response = self.client.post(reverse('nuova_transazione'), post_data)
        # controllo che il credito venga scalato
        # controllo che su transazioni ci sia la nuova transazione

    def test_nuova_transazione_verso_se_stesso(self):
        None

    def test_nuova_transazione_destinatario_non_ha_conto(self):
        None

    def test_nuova_transazione_credito_insufficente(self):
        None


class UtenteCheAccedeAlDettaglioDellaTransazione(TestCase):
    def test_get_page_owner_user(self):
        None

    def test_get_page_not_owner_user(self):
        None

    def test_get_page_transazione_non_esiste(self):
        None

    def test_redirect_on_detail_after_creation(self):
        None