from django.test import TestCase
from django.urls import reverse
from dashboard.models import *
from transazioni.forms import *

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

    def test_get_page_logged_user(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('transazioni'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transazioni.html')
        self.assertEqual(response.context['user'], self.mario)
        self.assertEqual(response.context['transazioni'].length, 0)

    def test_get_page_unlogged_user(self):
        response = self.client.get(reverse('transazioni'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'login.html')

    def test_transazioni_list(self):
        transazione = Transazione.objects.create(
            id_transazione='asfbsdaibuieb21', valuta=self.BTC,
            input_wallet=self.mario_wallet, output_wallet=self.luigi_wallet)
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('transazioni'))
        self.assertEqual(response.context['transazioni'].length, 1)
        self.assertEqual(response.context['transazioni'], transazione)

class UtenteCheCreaUnaTransazione(TestCase):
    def setUp(self):
        self.BTC = Valuta.objects.create(codice='BTC', cambio=8000, nome='Bitcoin')
        self.USD = Valuta.objects.create(codice='USD', cambio=1, nome='Dollaro')
        self.mario = User.objects.create_user(username='mariorossi', password='MarioRossi00')
        self.luigi = User.objects.create_user(username='luigibiasi', password='LuigiBiasi01')
        self.mario_wallet = Wallet.objects.create(user_id=self.mario, valuta_predefinita=self.USD)
        self.luigi_wallet = Wallet.objects.create(user_id=self.luigi, valuta_predefinita=self.USD)
        self.conto_btc_mario = Conto.objects.create(wallet_id=self.mario_wallet, quantita=1.0, valuta=self.BTC)
        self.conto_btc_luigi = Conto.objects.create(wallet_id=self.luigi_wallet, quantita=0.0, valuta=self.BTC)
        self.transazione = Transazione.objects.create(
            id_transazione='asfbsdaibuieb21',valuta=self.BTC,
            input_wallet=self.mario_wallet, output_wallet=self.wal)

    def test_get_page_logged_user(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('nuova_transazione'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nuova_transazione.html')
        self.assertEqual(response.context['user'], self.mario)
        self.assertEqual(response.context['form'], TransazioneForm)

    def test_get_page_unlogged_user(self):
        response = self.client.get(reverse('nuova_transazione'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'login.html')

    def test_nuova_transazione(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        data={'': 0}
        form_data = TransazioneForm(data)
        response = self.client.post(reverse('nuova_transazione'), form_data)
        # controllo che il credito venga scalato
        self.assertEqual(self.conto_btc_mario.importo,'tot')
        # controllo che su transazioni ci sia la nuova transazione
        self.client.get(reverse('transazioni'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['transazioni'].length, 2)
        transazione=Transazione.objects.get(data)
        self.assertEqual(response.context['transazioni'][1], transazione)


    def test_nuova_transazione_verso_se_stesso(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        data = {'': 0}
        form_data = TransazioneForm(data)
        response = self.client.post(reverse('nuova_transazione'), form_data)
        self.assertRedirects(response,reverse('nuova_transazione'))
        self.assertContains(response.context['message'],'non puoi verso te stesso')
        self.assertEqual(response.context['form'],form_data)
        self.assertRaises(ObjectNotFoundException, Transazione.objects.get(data))

    def test_nuova_transazione_destinatario_non_ha_conto(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        data = {'': 0}
        form_data = TransazioneForm(data)
        self.assertRaises(ObjectNotFoundException, Conto.objects.get(valuta=data.valuta,wallet_id=data.destination_wallet))
        response = self.client.post(reverse('nuova_transazione'), form_data)
        self.assertEqual(Conto.objects.get(valuta=data.valuta,wallet_id=data.destination_wallet).importo,data.importo)

    def test_nuova_transazione_credito_insufficente(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        data = {'': 0}
        form_data = TransazioneForm(data)
        response = self.client.post(reverse('nuova_transazione'), form_data)
        self.assertRedirects(response, reverse('nuova_transazione'))
        self.assertContains(response.context['message'], 'non hai abbastanza credito')
        self.assertEqual(response.context['form'], form_data)
        self.assertRaises(ObjectNotFoundException, Transazione.objects.get(data))

    def test_redirect_on_detail_after_creation(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        data = {'': 0}
        form_data = TransazioneForm(data)
        response = self.client.post(reverse('nuova_transazione'), form_data)
        self.assertRedirects(response, reverse('dettaglio_transazione',Transazione.objects.get(data)))


class UtenteCheAccedeAlDettaglioDellaTransazione(TestCase):
    def setUp(self):
        self.BTC = Valuta.objects.create(codice='BTC', cambio=8000, nome='Bitcoin')
        self.USD = Valuta.objects.create(codice='USD', cambio=1, nome='Dollaro')
        self.mario = User.objects.create_user(username='mariorossi', password='MarioRossi00')
        self.luigi = User.objects.create_user(username='luigibiasi', password='LuigiBiasi01')
        self.nessuno = User.objects.create_user(username='nessuno', password='nessuno21')

        self.mario_wallet = Wallet.objects.create(user_id=self.mario, valuta_predefinita=self.USD)
        self.luigi_wallet = Wallet.objects.create(user_id=self.luigi, valuta_predefinita=self.USD)
        self.conto_btc_mario = Conto.objects.create(wallet_id=self.mario_wallet, quantita=1.0, valuta=self.BTC)
        self.conto_btc_luigi = Conto.objects.create(wallet_id=self.luigi_wallet, quantita=0.0, valuta=self.BTC)
        self.transazione = Transazione.objects.create(
            id_transazione='asfbsdaibuieb21', valuta=self.BTC,
            input_wallet=self.mario_wallet, output_wallet=self.wal)


    def test_get_page_owner_user(self):
        self.client.login(username="mariorossi", password="MarioRossi00")
        response = self.client.get(reverse('dettaglio_transazione', self.transazione))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dettaglio_transazione.html')
        self.assertEqual(response.context['transazione'], self.transazione)

    def test_get_page_not_owner_user(self):
        self.client.login(username='nessuno', password='nessuno21')
        response = self.client.get(reverse('dettaglio_transazione', self.transazione))
        self.assertRedirects(response, reverse('transazioni'))
        self.assertTemplateUsed(response, 'transazioni.html')
        self.assertContains(response.context['message'], 'non hai i permessi')

    def test_get_page_transazione_non_esiste(self):
        self.client.login(username='nessuno', password='nessuno21')
        response = self.client.get(reverse('dettaglio_transazione',))
        self.assertRedirects(response, reverse('transazioni'))
        self.assertTemplateUsed(response, 'transazioni.html')
        self.assertContains(response.context['message'], 'non esiste')

