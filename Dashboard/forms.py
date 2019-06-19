from django import forms
from .models import Wallet, Conto
from django.contrib.admin.widgets import FilteredSelectMultiple


class WalletAdminForm(forms.ModelForm):
    conti = forms.ModelMultipleChoiceField(
        queryset=Conto.objects.all(),
        widget=FilteredSelectMultiple(verbose_name='conti', is_stacked=False,))

    class Meta:
        model = Wallet
        fields = ['wallet_id', 'user_id', 'cambio_selezionato']

    def __init__(self, *args, **kwargs):
        super(WalletAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            # fill initial related values
            self.fields['conti'].initial = self.instance.conti.all()
            # prevent editing conti
            self.fields['conti'].disabled = True
