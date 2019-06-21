from django.db import models


#class Transazione(models.Model):
#    id_transazione = models.CharField(max_length=32, null=False, unique=True)
#    data = models.DateTimeField(auto_now=True)
#    input_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='input_wallet_id')
#    output_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='output_wallet_id')
#    cryptocurrency = models.ForeignKey(Valuta, on_delete=models.CASCADE)
#    quantita = models.DecimalField(decimal_places=15, max_digits=30)

#    @staticmethod
 #   def crea_transazione(wallet_input,wallet_output,tipo_valuta,importo):
#        None

 #   def get_url(self):  #restituisce l'url dell'istanza della transazione
    #    None

  #  def str(self):
   #     return self.id_transazione