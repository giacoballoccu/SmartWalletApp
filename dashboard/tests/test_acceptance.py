from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from dashboard.models import *


class UtenteCheAccedeAllaPropriaDashboard(TestCase):

    '''
    def setUpTestData(cls):
        cls.mario = User.objects.create(username="mariorossi", password="MarioRossi00")
        cls.luigi = User.objects.create(username="luigibiasi", password="LuigiBiasi01")
        cls.wallet_mario = Wallet.objects.create(user_id=cls.mario)
        cls.wallet_luigi = Wallet.objects.create(user_id=cls.luigi)
    '''

    def test_get_page_logged_user(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertIsNotNone(response.context['user'])

    def test_get_page_unlogged_user(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'login.html')

    def test_conti_list(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertIsNotNone(response.context['conti'])
        # controllo lunghezza array conti

    def test_totale_wallet(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertIsNotNone(response.context['totale_wallet'])
        # controllo esattezza risultato

    def test_modifica_valuta_predefinita(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.post(
            reverse('modifica_valuta_predefinita'), {'valuta': 'BTC'})
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(response.context['valuta_predefinita'], 'BTC')


class UtenteCheAggiungeRimuoveUnConto(TestCase):
    def test_get_page_aggiunta_conto(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('aggiungi_conto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aggiungi_conto.html')
        self.assertIsNotNone(response.context['form'])

    def test_post_page_aggiunta_conto(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        data = {'valuta': 'BTC', 'importo': 1}
        form_data = form_aggiunta_conto(data)
        response = self.client.post(reverse('aggiungi_conto'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response.context['conti'], Conto(data))

    def test_post_page_aggiunta_conto_gia_esistente(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        data = {'valuta': 'USD', 'importo': 10}
        form_data = form_aggiunta_conto(data)
        response = self.client.post(reverse('aggiungi_conto'), form_data)
        self.assertEqual(response.status_code, -1)
        self.assertTemplateUsed(response, 'aggiungi_conto.html')
        self.assertIsNotNone(response.context['error_msg'])
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertNotContains(response.context['conti'], Conto(data))

    def test_get_page_modifica_conto(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('modifica_conto', {'valuta': 'BTC'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modifica_conto.html')
        self.assertEqual(response.context['form'], -1)

    def test_get_page_modifica_conto_non_esistente(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('modifica_conto', {'valuta': 'USD'}))
        self.assertEqual(response.status_code, -1)
        self.assertIsNotNone(response.context['error_msg'])

    def test_post_page_rimozione_conto(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        data={'valuta': 'BTC', 'remove': True}
        form_data = form_modifica_coto(data)
        response = self.client.post(reverse('modifica_conto'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertNotContains(response.context['conti'], Conto(valuta='BTC'))

    def test_post_modifica_importo(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        data = {'valuta': 'BTC', 'importo': 2}
        form_data = form_modifica_coto(data)
        response = self.client.post(reverse('modifica_conto'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertEqual(response.context['conti'].importo, Conto(data))
