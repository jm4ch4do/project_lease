from django.db import models
from app_lease.models import Customer, Trade


class Proposal(models.Model):

    # foreign keys
    trade = models.ForeignKey(Trade, blank=False, on_delete=models.CASCADE)
    created_by_customer = models.ForeignKey(Customer, blank=False, on_delete=models.CASCADE,
                                            related_name='created_by_customer')
    accepted_by_customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.CASCADE
                                             , related_name='accepted_by_customer')

    # ----- string fields
    note = models.TextField(blank=True, null=True, max_length=200)
    system_note = models.TextField(blank=True, null=True, max_length=200)

    # ----- numeric fields
    total_amount = models.FloatField(blank=False)
    total_days_to_pay = models.IntegerField(blank=False, default=0)
    down_payment = models.FloatField(blank=False)

    # ----- flags
    CHOICES_PROPOSAL_STATUS = (
        (1, 'pending'),  # not decided yet
        (2, 'accepted'),   # proposal wins the trade
        (3, 'refused'),   # owner refused the proposal
        (4, 'closed'),    # parent trade was canceled or another proposal was accepted
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
        if self.total_time_to_pay < 30:
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

    # ----- functions
    def accept_proposal(self):
        pass
        # proposal can't be accepted if trade is already accepted

        # close proposal

        # accept trade

        # close other proposals for same trade leaving a note

    def refuse_proposal(self):
        pass
        # change state to refused and leave a note

    # ----- string output
    def __str__(self):
        return self.proposed_by + ' proposes ' + str(self.total_amount) + \
               ' as ' + self.get_pay_frequency_display() + ' for ' + str(self.trade)
