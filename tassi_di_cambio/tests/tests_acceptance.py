from django.test import TestCase
from django.urls import reverse
from dashboard.models import *

class UtenteAccedeAllaSezioneConversioneValuta(TestCase):
    def setUp(self):
        self.BTC= Valuta.objects.create(codice='BTC', cambio=8000.0,nome='Bitcoin')
        self.USD= Valuta.objects.create(codice='USD', cambio=1.0, nome='Dollaro')

    def test_get_page_logged_user(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('tassi_di_cambio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'convertitore.html')
        self.assertEqual(response.context['user'], self.mario)
        self.assertEqual(response.context['form'],'?')

    def test_get_page_unlogged_user(self):
        response = self.client.get(reverse('tassi_di_cambio'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'login.html')

    def test_post_conversion_request(self):
        self.assertTrue(False)