from django.db import models
from app_lease.models import Trade, Customer, Payment
from datetime import datetime, timedelta
from django.db.models import Sum
from django.core.exceptions import ValidationError


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

    # ----- calculations
    @property
    def label(self):
        return '$' + str(self.amount) + " on " + self.customer.name + " for trade: " + str(self.trade)

    @property
    def days_remaining(self):
        date_diff = self.due_date - datetime.now().date()
        return date_diff.days

    @property
    def left_to_pay(self):
        paid = 0 if not self.payment_set.all() else self.payment_set.all().aggregate(Sum('amount'))
        return self.amount - paid

    # ----- functions
    def pay_invoice(self, credit_card, payment_amount=None):

        # can't pay if there is nothing owed
        if self.left_to_pay == 0:
            raise ValidationError(
                "Can't paid because there is nothing owed",
                code='paying_already_paid_invoice'
            )

        # can't pay more than left_to_pay
        if payment_amount and payment_amount > self.left_to_pay:
            raise ValidationError(
                "Can't pay more than amount owed which is " + str(self.left_to_pay),
                code='overpaying_invoice'
            )

        # no amount specified to pay -> pay maximum
        payment_amount = self.left_to_pay if not payment_amount else payment_amount

        # create payment
        created_payment = Payment.objects.create(
            creditcard=credit_card,
            invoice=self,
            amount=payment_amount,
        )


    # string output
    def __str__(self):
        return self.label
