from app_lease.models import Invoice
from django.core.exceptions import ValidationError


# ----- functions
def accept_proposal(proposal, accepting_customer):

    # proposal can't be accepted if trade is already accepted
    if proposal._status == 2:
        raise ValidationError(
            "Proposal was already previously accepted already accepted",
            code='already_accepted_proposal',
        )

    # close proposal and trade
    proposal.accepted_by_customer = accepting_customer
    proposal._status = 2
    proposal.save()
    proposal.trade.status = 2
    proposal.trade.save()

    # close other proposals for same trade leaving a note
    for a_proposal in proposal.trade.proposal_set.all():
        if a_proposal != proposal:
            a_proposal._status = 4
            a_proposal.system_note = 'closed because other proposal was approved'
            a_proposal.save()

    # if trade is sale then create invoice
    if proposal.trade.service.service_type == 2:
        Invoice.objects.create(
            trade=proposal.trade,
            customer=proposal.trade.vehicle.customer,
            amount=proposal.trade.service.cost,
            system_note='for accepting proposal for service sale'
        )


def refuse_proposal(proposal):

    # proposal can only be refused by owner if was created by buyer
    if proposal.created_by_customer == proposal.trade.vehicle.customer:
        raise ValidationError(
            "Owner can't refuse its own proposal. You should try canceling proposal.",
            code='owner_refusing_own_proposal',
        )

    # change state to refused and leave a note
    proposal._status = 3
    proposal.system_note = 'owner refused the proposal'
    proposal.save()


def cancel_proposal(proposal):

    # proposal can only be canceled by owner if was created by owner
    if proposal.created_by_customer != proposal.trade.vehicle.customer:
        raise ValidationError(
            "Owner can't cancel other customer's proposal. You should try refusing proposal.",
            code='owner_canceling_customer_proposal',
        )

    # change state to canceled and leave a note
    proposal._status = 5
    proposal.system_note = 'owner canceled the proposal'
    proposal.save()
