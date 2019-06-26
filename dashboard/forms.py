from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Wallet, Conto
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext as _


class WalletAdminForm(forms.ModelForm):
   # conti = forms.ModelMultipleChoiceField(
   #     queryset=Conto.objects.all(),
    #    widget=FilteredSelectMultiple(verbose_name='conti', is_stacked=False,))

    class Meta:
        model = Wallet
        fields = ['wallet_id', 'user_id', 'cambio_selezionato', 'ultimo_aggiornamento']

    def __init__(self, *args, **kwargs):
        super(WalletAdminForm, self).__init__(*args, **kwargs)
        #if self.instance:
        #    # fill initial related values
        #    self.fields['conti'].initial = self.instance.conti.all()
        #    # prevent editing conti
        #    self.fields['conti'].disabled = True

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password2 = forms.PasswordInput()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

class NewContoForm(forms.ModelForm):

    class Meta:
        model = Conto
        fields = ['tipo_valuta']


    def __init__(self, *args, **kwargs):
        super(NewContoForm, self).__init__(*args, **kwargs)
