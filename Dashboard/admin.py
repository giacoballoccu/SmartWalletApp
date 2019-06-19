from django.contrib import admin
from .models import Wallet, Conto, Valuta, Transazione
from .forms import WalletAdminForm


class WalletAdmin(admin.ModelAdmin):
    form = WalletAdminForm


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Conto)
admin.site.register(Valuta)
admin.site.register(Transazione)
