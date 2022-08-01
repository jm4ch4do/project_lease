from django.db import models
from app_lease.models import Trade, Customer
from datetime import datetime, timedelta


class Invoice(models.Model):

    # foreign keys
    trade = models.OneToOneField(Trade, blank=False, on_delete=models.CASCADE)
    customer = models.OneToOneField(Customer, blank=False, on_delete=models.CASCADE)

    # string fields
    system_note = models.CharField(blank=True, null=True, max_length=500)

    # numeric fields
    amount = models.FloatField(blank=False)

    # flags
    CHOICES_INVOICE_STATUS = (
        (1, 'pending'),
        (2, 'paid'),
    )
    _status = models.SmallIntegerField(choices=CHOICES_INVOICE_STATUS, default=1)

    # date fields
    TODAY_PLUS_30DAYS = (datetime.now() + timedelta(30)).date()
    due_date = models.DateField(blank=False, default=TODAY_PLUS_30DAYS)

    # internal fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # calculation
    @property
    def label(self):
        return '$' + str(self.amount) + " on " + self.customer.name + " for trade: " + str(self.trade)

    @property
    def days_remaining(self):
        date_diff = self.due_date - datetime.now().date()
        return date_diff.days

    # string output
    def __str__(self):
        return self.label
