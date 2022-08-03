from django.core.exceptions import ValidationError
from app_lease.models import Trade, Invoice


def cancel_trade(trade):

    # trade can't be canceled if it was already accepted
    if trade.status == 2:
        raise ValidationError(
            "Can't cancel trade that was already accepted.",
            code='canceling_accepted_trade',
        )

    # cancel trade
    trade.status = 3
    trade.save()

    # close related proposals
    for a_proposal in trade.proposal_set.all():
        a_proposal._status = 4
        a_proposal.system_note = 'Closed because trade was canceled'
        a_proposal.save()


def create_trade(service, vehicle):

    created_trade = Trade.objects.create(
        service=service,
        vehicle=vehicle,
    )

    # An invoice should be created if service type is lease,
    if service.service_type == 1:
        Invoice.objects.create(
            trade=created_trade,
            customer=created_trade.vehicle.customer,
            amount=service.cost,
            system_note='for creating trade type lease'
        )
