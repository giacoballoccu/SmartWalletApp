from django.test import TestCase
from django.contrib.auth.models import User
from dashboard.models import Valuta


class ValutaModelTest(TestCase):
    def setUp(self):
        self.dollaro = Valuta.objects.create(sigla="USD", cambio="1.0", nome="Dollaro")
        self.bitcoin = Valuta.objects.create(sigla="BTC", cambio="8000.0", nome="Bitcoin")
        self.euro = Valuta.objects.create(sigla="EUR", cambio="1.2", nome="Euro")

    def test_sigla_field(self):
        # controlla che sia massimo 3 caratteri
        max_lenght = self.dollaro._meta.get_field("sigla").max_length
        self.assertEqual(max_lenght, 3)
        # controlla che abbia il giusto valore
        self.assertEqual('USD', self.dollaro.sigla)
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

