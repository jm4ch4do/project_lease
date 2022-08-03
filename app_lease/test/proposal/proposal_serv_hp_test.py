import pytest
from app_lease.test.generator import random_proposal, random_customer
from app_lease.services.proposal_serv import accept_proposal, refuse_proposal, cancel_proposal


@pytest.mark.order(9)
@pytest.mark.django_db
def test_buyer_accepts_proposal():
    """ Accepting a proposal changes status of all proposals related to parent trade.
        Test buyer accepting owner proposal.
    """

    # two customers come to shop
    created_customer2 = random_customer()
    created_customer3 = random_customer()

    # owner makes two proposals
    created_proposal1 = random_proposal()
    created_proposal2 = random_proposal(trade=created_proposal1.trade)

    # customer3 makes proposal
    created_proposal3 = random_proposal(trade=created_proposal1.trade, created_by_customer=created_customer3)

    # customer2 accepts proposal1
    accept_proposal(created_proposal1,created_customer2)

    # refresh models from database
    created_proposal1.refresh_from_db(), created_proposal2.refresh_from_db(), created_proposal3.refresh_from_db(),

    # ----- results
    # buyer was properly assign
    assert True if created_proposal1.accepted_by_customer == created_customer2 else False

    # status changed on trade and all proposals for the same trade
    assert True if created_proposal1._status == 2 else False  # proposal accepted
    assert True if created_proposal1.trade.status == 2 else False  # trade accepted
    assert True if created_proposal2._status == 4 else False  # proposal closed (not accepted)
    assert True if isinstance(created_proposal2.system_note, str) else False  # system_note in closed proposal
    assert True if created_proposal3._status == 4 else False  # proposal closed (not accepted)
    assert True if isinstance(created_proposal3.system_note, str) else False  # system_note in closed proposal


@pytest.mark.order(9)
@pytest.mark.django_db
def test_owner_accepts_proposal():
    """ Accepting a proposal changes status of all proposals related to parent trade.
        Test owner accepting buyers proposal.
    """

    # two customers come to shop
    created_customer2 = random_customer()
    created_customer3 = random_customer()

    # owner makes two proposals
    created_proposal1 = random_proposal()
    created_proposal2 = random_proposal(trade=created_proposal1.trade)

    # customer3 makes proposal
    created_proposal3 = random_proposal(trade=created_proposal1.trade, created_by_customer=created_customer3)

    # owner accepts proposal3
    owner = created_proposal1.trade.vehicle.customer
    accept_proposal(created_proposal3, owner)

    # refresh models from database
    created_proposal1.refresh_from_db(), created_proposal2.refresh_from_db(), created_proposal3.refresh_from_db(),

    # ----- results
    # owner was properly assign
    assert True if created_proposal3.accepted_by_customer == owner else False

    # status changed on trade and all proposals for the same trade
    assert True if created_proposal3._status == 2 else False  # proposal accepted
    assert True if created_proposal3.trade.status == 2 else False  # trade accepted
    assert True if created_proposal1._status == 4 else False  # proposal closed (not accepted)
    assert True if isinstance(created_proposal1.system_note, str) else False  # system_note in closed proposal
    assert True if created_proposal2._status == 4 else False  # proposal closed (not accepted)
    assert True if isinstance(created_proposal2.system_note, str) else False  # system_note in closed proposal


@pytest.mark.order(9)
@pytest.mark.django_db
def test_owner_refuses_proposal():
    """ Owner can refuse a proposal from another customer
    """

    # one customer comes to shop
    created_customer2 = random_customer()

    # owner makes a proposal
    created_proposal1 = random_proposal()
    owner = created_proposal1.trade.vehicle.customer

    # customer2 makes proposal
    created_proposal2 = random_proposal(trade=created_proposal1.trade, created_by_customer=created_customer2)

    # owner refuses proposal2
    refuse_proposal(created_proposal2)

    # refresh model from database
    created_proposal2.refresh_from_db()

    # ----- results
    # proposal is refused and has system_note
    assert True if created_proposal2._status == 3 else False
    assert True if isinstance(created_proposal2.system_note, str) else False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_owner_canceling_own_proposal():
    """ Owner can cancel some his own proposal """

    # owner makes a proposal
    created_proposal = random_proposal()

    # owner cancels his own proposal
    cancel_proposal(created_proposal)

    # refresh model from database
    created_proposal.refresh_from_db()

    # check proposal was canceled
    assert True if created_proposal._status == 5 else False
    assert True if isinstance(created_proposal.system_note, str) else False  # note after canceling
