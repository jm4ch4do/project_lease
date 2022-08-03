from django.core.exceptions import ValidationError


def create_trade():
    pass


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
