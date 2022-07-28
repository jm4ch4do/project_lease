from faker import Faker
from app_lease.utils.fake_provider import Provider
from app_lease.test.generator import random_trade
from app_lease.models import Proposal
from random import uniform, randint


def random_proposal(total=1, trade=None, created_by_customer=None):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # ----- create proposals
    created_proposals = []
    for _ in range(total):

        # create trade if needed
        created_trade = trade if trade else random_trade()

        # create customer if needed
        created_by_customer = created_by_customer if created_by_customer else created_trade.vehicle.customer

        # proposal parameters
        total_amount = round(uniform(10_000, 40_000), 0)
        down_payment = total_amount if created_trade.service.service_type == 2 else total_amount / 5
        total_days_to_pay = 0 if created_trade.service.service_type == 2 else randint(90, 1080)
        pay_frequency = 1 if created_trade.service.service_type == 2 else randint(2, 4)

        # create proposal
        created_proposal = Proposal.objects.create(
            trade=created_trade,
            created_by_customer=created_by_customer,
            total_amount=total_amount,
            down_payment=down_payment,
            total_days_to_pay=total_days_to_pay,
            pay_frequency=pay_frequency,
        )

        created_proposals.append(created_proposal)

    if len(created_proposals) == 1:
        return created_proposal
    else:
        return created_proposals
