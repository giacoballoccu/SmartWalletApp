from django.test import TestCase
from django.urls import reverse
from ..forms import *
from django.contrib.auth.models import User

from dashboard.models import *


class UtenteCheAccedeAllaPropriaDashboard(TestCase):
    def setUp(self):
        self.BTC = Valuta.objects.create(sigla='BTC', cambio=8000, nome='Bitcoin')
        self.USD = Valuta.objects.create(sigla='USD', cambio=1, nome='Dollaro')
        self.mario = User.objects.create_user(username='mariorossi', password='MarioRossi00')
        self.mario_wallet = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.USD)
        self.conto_btc_mario = Conto.objects.create(wallet_associato=self.mario_wallet, importo=1.0, tipo_valuta=self.BTC)

    def test_get_page_logged_user(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(response.context['user'], self.mario)

    def test_get_page_unlogged_user(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'logout.html')

    def test_conti_list(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertIsNotNone(response.context['conti'])
        # controllo esattezza array conti passati al template
        self.assertEqual(len(response.context['conti']), 1)
        self.assertEqual(response.context['conti'][0].tipo_valuta, self.BTC)
        self.assertEqual(response.context['conti'][0].importo, 1)

    def test_totale_wallet(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(response.context['totale'], '%.9f' % (self.conto_btc_mario.importo*self.BTC.cambio))

    def test_modifica_tipo_valuta_predefinita(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.post(
            reverse('selezione_cambio'), {'tipo_valuta': self.BTC})
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(response.context['cambio_selezionato'], self.BTC)
        self.assertEqual(response.context['totale_wallet'], self.conto_btc_mario.importo)


class UtenteCheAggiungeUnConto(TestCase):
    def setUp(self):
        self.BTC= Valuta.objects.create(sigla='BTC', cambio=8000,nome='Bitcoin')
        self.USD= Valuta.objects.create(sigla='USD', cambio=1, nome='Dollaro')
        self.mario = User.objects.create_user(username='mariorossi',password='MarioRossi00')
        self.luigi = User.objects.create_user(username='luigibiasi',password='LuigiBiasi01')
        self.mario_wallet = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.USD)
        self.conto_btc_mario = Conto.objects.create(wallet_associato=self.mario_wallet, importo=0.0, tipo_valuta=self.BTC)

    def test_get_page_aggiunta_conto(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('aggiungi_conto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aggiungi_conto.html')
        self.assertEqual(response.context['form'], NewContoForm)

    def test_post_page_aggiunta_conto(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        data = {'tipo_valuta': self.USD}
        form_data = NewContoForm(data = data)
        response = self.client.post(reverse('aggiungi_conto'), form_data)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(response.context['conti'], Conto.objects.get(wallet_associato=self.mario_wallet,tipo_valuta=self.USD))

    def test_post_page_aggiunta_conto_gia_esistente(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.post("/aggiungi_conto", {'tipo_valuta': self.BTC})
        self.assertRedirects(response, reverse('aggiungi_conto'))
        self.assertTemplateUsed(response, 'aggiungi_conto.html')
        self.assertIsNotNone(response.context['message'])
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertNotContains(len(response.context['conti']),2)

class UtenteCheRimuoveUnConto(TestCase):
    def setUp(self):
        self.BTC = Valuta.objects.create(sigla='BTC', cambio=8000, nome='Bitcoin')
        self.USD = Valuta.objects.create(sigla='USD', cambio=1, nome='Dollaro')
        self.mario = User.objects.create_user(username='mariorossi', password='MarioRossi00')
        self.luigi = User.objects.create_user(username='luigibiasi', password='LuigiBiasi01')
        self.mario_wallet = Wallet.objects.create(user_id=self.mario, cambio_selezionato=self.USD)
        self.luigi_wallet = Wallet.objects.create(user_id=self.luigi, cambio_selezionato=self.USD)
        self.conto_btc_mario = Conto.objects.create(wallet_associato=self.mario_wallet, importo=0.0, tipo_valuta=self.BTC)
        self.conto_usd_mario = Conto.objects.create(wallet_associato=self.mario_wallet, importo=0.0, tipo_valuta=self.USD)
        self.conto_btc_luigi = Conto.objects.create(wallet_associato=self.luigi, importo=0.0, tipo_valuta=self.BTC)

    def test_post_page_rimozione_conto(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.post(reverse('rimuovi_conto',self.conto_btc_mario))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertNotContains(response.context['conti'], self.conto_btc_mario)

    def test_post_page_rimuovi_conto_non_esistente(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('rimuovi_conto', {'conto_id': 'none'}))
        self.assertEqual(response.status_code, -1)
        self.assertContains(response.context['message'])

    def test_post_page_rimuovi_conto_non_in_proprio_possesso(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.post(reverse('rimuovi_conto', self.conto_btc_luigi))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response.context['conti'], Conto(tipo_valuta=self.BTC))
        self.assertContains(response.context['message'],'non è il tuo conto')

    def test_post_page_rimuovi_conto_non_vuoto(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.post(reverse('rimuovi_conto', self.conto_usd_mario))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response.context['conti'], self.conto_usd_mario)
        self.assertContains(response.context['message'],'conto non vuoto')



