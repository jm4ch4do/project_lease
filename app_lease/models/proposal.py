from django.db import models
from app_lease.models import Customer, Trade


class Proposal(models.Model):

    # foreign keys
    trade = models.ForeignKey(Trade, blank=False, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.CASCADE)

    # numeric fields
    total_amount = models.FloatField(blank=False)
    total_time_to_pay = models.IntegerField(blank=False, default=0)
    down_payment = models.IntegerField(blank=False)

    # flags
    CHOICES_PROPOSAL_STATUS = (
        (1, 'pending'),  # proposal wins the trade
        (2, 'accepted'),   # not decided yet
        (3, 'refused'),   # owner refused the proposal
        (4, 'closed'),    # parent trade was canceled or another proposal was accepted
    )
    status = models.SmallIntegerField(blank=False, choices=CHOICES_PROPOSAL_STATUS, default=1)

    CHOICES_TRADE_PAY_FREQUENCY = (
        (1, 'one_time'),
        (2, 'monthly'),
        (3, 'biweekly'),
        (4, 'weekly'),
    )
    pay_frequency = models.SmallIntegerField(blank=False, choices=CHOICES_TRADE_PAY_FREQUENCY, default=1)

    # calculations
    @property
    def proposed_by(self):
        return "owner" if not self.customer else "buyer"

    @property
    def monthly_payment(self):

        # only one time payment => no monthly_payment
        if self.total_amount == self.down_payment:
            return 0

        # time to pay lower than a month => assume one month
        if self.total_time_to_pay < 30:
            return self.total_amount - self.down_payment

        return (self.total_amount - self.down_payment)/30

    @property
    def bi_weekly_payment(self):

        return self.monthly_payment/2

    @property
    def weekly_payment(self):

        return self.monthly_payment/4
