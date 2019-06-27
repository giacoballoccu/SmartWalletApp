from django.test import TestCase
from django.urls import reverse
from dashboard.models import *


class UtenteAccedeAllaSezioneConversioneValuta(TestCase):
    def setUp(self):
        self.mario = User.objects.create_user(username="mariorossi", password="MarioRossi00")
        self.BTC = Valuta.objects.create(sigla='BTC', cambio=8000.0, nome='Bitcoin')
        self.USD = Valuta.objects.create(sigla='USD', cambio=1.0, nome='Dollaro')
        Wallet.crea_wallet(get_random_string(length=32),self.mario, self.USD)

    def test_get_page_logged_user(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('converti_valute'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'convertivalute.html')
        self.assertEqual(response.context['user'], self.mario)


    def test_get_page_unlogged_user(self):
        response = self.client.get(reverse('converti_valute'))
        self.assertEqual(response.status_code, 302)
