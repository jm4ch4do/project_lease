from django.db import models
from app_lease.models import Customer, Service, Vehicle


class Trade(models.Model):

    # foreign keys
    service = models.ForeignKey(Service, blank=False, on_delete=models.CASCADE)
    vehicle = models.OneToOneField(Vehicle, blank=False, on_delete=models.CASCADE)

    # string fields
    note = models.CharField(blank=True, null=True, max_length=500)

    # flags
    CHOICES_TRADE_STATUS = (
        (1, 'open'),
        (2, 'closed'),
        (3, 'canceled'),
    )
    status = models.SmallIntegerField(choices=CHOICES_TRADE_STATUS)

    # internal fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        # ordering
        ordering = ['created_at']

        # ----- constraints
        # vehicle and service are unique as a couple
        constraints = [
            models.UniqueConstraint(fields=['vehicle', 'service'], name='unique_vehicle_service_in_trade'),
        ]

    # calculation
    @property
    def label(self):
        return self.vehicle.name + " /" + str(self.vehicle.customer.name) + "/" \
                                 + " [" + str(self.service.name) + "]"

    # string output
    def __str__(self):
        return self.label


# service ID
# customer ID
# status - open, closed, canceled
# vehicle ID
#


# Proposals
# tradeID
# customer ID
# type - Owner, Buyer
# status - Accepted, Pending, Refused
# totalamount
# totaltime
# downpayment
# monthlypay
# @weeklypay
# @dailypay


# Invoice
# tradeID
# amount

# Payment
# Amount
# invoiceID


