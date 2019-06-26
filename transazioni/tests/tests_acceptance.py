from django.test import TestCase


class UtenteAccedeAllaSezioneTransazioni(TestCase):
    def test_get_page_logged_user(self):
        None

    def test_get_page_unlogged_user(self):
        None

    def test_transazioni_list(self):
        None


class UtenteCheCreaUnaTransazione(TestCase):
    def test_get_page_logged_user(self):
        None

    def test_get_page_unlogged_user(self):
        None

    def test_post_page_nuova_transazione(self):
        None


class UtenteCheAccedeAlDettaglioDellaTransazione(TestCase):
    def test_get_page_owner_user(self):
        None

    def test_get_page_not_owner_user(self):
        None

    def test_redirect_on_detail_after_creation(self):
        None