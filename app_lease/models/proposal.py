from django.db import models
from app_lease.models import Customer, Trade
from app_lease.validators import repeated_values, value_contained


class Proposal(models.Model):

    # foreign keys
    trade = models.ForeignKey(Trade, blank=False, on_delete=models.CASCADE)
    created_by_customer = models.ForeignKey(Customer, blank=False, on_delete=models.CASCADE, related_name='created_by_customer')
    accepted_by_customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.CASCADE,
                                             related_name='accepted_by_customer')

    # ----- string fields
    note = models.TextField(blank=True, null=True, max_length=200)
    system_note = models.TextField(blank=True, null=True, max_length=200)

    # ----- numeric fields
    total_amount = models.FloatField(blank=False)
    total_days_to_pay = models.IntegerField(blank=False, default=0)
    down_payment = models.FloatField(blank=False)

    # ----- flags
    CHOICES_PROPOSAL_STATUS = (
        (1, 'pending'),   # not decided yet
        (2, 'accepted'),  # proposal wins the trade
        (3, 'refused'),   # owner refused the proposal
        (4, 'closed'),    # parent trade was canceled or another proposal was accepted
        (5, 'canceled'),  # owner canceled his own offer
    )
    _status = models.SmallIntegerField(blank=False, choices=CHOICES_PROPOSAL_STATUS, default=1)

    CHOICES_TRADE_PAY_FREQUENCY = (
        (1, 'one_time'),
        (2, 'monthly'),
        (3, 'biweekly'),
        (4, 'weekly'),
    )
    pay_frequency = models.SmallIntegerField(blank=False, choices=CHOICES_TRADE_PAY_FREQUENCY, default=1)

    # ----- calculations
    @property
    def proposed_by(self):
        return "owner" if self.created_by_customer == self.trade.vehicle.customer else "buyer"

    @property
    def monthly_payment(self):

        # only one time payment => no monthly_payment
        if self.total_amount == self.down_payment:
            return float(0)

        # time to pay lower than a month => assume one month
        if self.total_days_to_pay < 30:
            return self.total_amount - self.down_payment

        return (self.total_amount - self.down_payment)/30

    @property
    def bi_weekly_payment(self):

        return self.monthly_payment/2

    @property
    def weekly_payment(self):

        return self.monthly_payment/4

    @property
    def show_notes(self):

        # guarantee notes always contain string
        note = '' if not self.note else self.note
        system_note = '' if not self.system_note else self.system_note

        # output only note if no system_note
        if not self.system_note:
            return note
        else:
            return note + '\n' + '---system_note---\n' + system_note

    # validation
    def clean(self):

        # created_by_customer and accepted_by_customer can't have same user
        repeated_values([self.created_by_customer, self.accepted_by_customer],
                        'created_by/accepted_by')

        # created_by_customer or accepted_by_customer must be the vehicle's owner
        value_contained([self.created_by_customer, self.accepted_by_customer],
                        self.trade.vehicle.customer, "vehicle's owner must be in created_by or accepted_by")



    # ----- string output
    def __str__(self):
        return self.proposed_by + ' proposes ' + str(self.total_amount) + \
               ' as ' + self.get_pay_frequency_display() + ' for ' + str(self.trade)
