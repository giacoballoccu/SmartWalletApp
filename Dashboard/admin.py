from django.contrib import admin
from .models import Wallet
from .models import Conto
from .models import Valuta
from .models import Transazione


#Not working

class ContoInLine(admin.TabularInline):
    model = Conto

class WalletAdmin(admin.ModelAdmin):
    inlines = [
        ContoInLine,
    ]
# Register your models here.

admin.site.register(Wallet)
admin.site.register(Conto)
admin.site.register(Valuta)
admin.site.register(Transazione)