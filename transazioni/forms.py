from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from dashboard.models import Transazione


class TransazioneForm(forms.ModelForm):

    class Meta:
        model = Transazione
        fields = ['output_wallet', 'cryptocurrency', 'quantita']


    def __init__(self, *args, **kwargs):
        super(TransazioneForm, self).__init__(*args, **kwargs)
