from django.db import models
from app_lease.models import CreditCard, Invoice


class Payment(models.Model):

    # foreign keys
    creditcard = models.OneToOneField(CreditCard, blank=False, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, blank=False, on_delete=models.CASCADE)

    # numeric fields
    amount = models.FloatField(blank=False)

    # internal fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def label(self):
        return str(self.amount) + ' to Invoice: ' + str(self.invoice) + \
               ' with card ending ' + str(self.creditcard.card_number)[-4:]
