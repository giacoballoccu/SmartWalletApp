from django.test import TestCase
from .models import Valuta,Conto,Wallet


class ValutaModelTest(TestCase):
    @classmethod
    def SetUpTestData(cls):
        Valuta.objects.create(sigla="USD", cambio="1.0", nome="Dollaro")
        Valuta.objects.create(sigla="BTC", cambio="8000.0", nome="BitCoin")

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
        # controlla che restituisca il valore giusto
        dollaro = Valuta.objects.get(sigla="USD")
        bitcoin = Valuta.objects.get(sigla="BTC")
        self.assertEqual(dollaro.converti_cambio('BTC'), 1.0 / 8000)
