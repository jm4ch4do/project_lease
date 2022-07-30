# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from app_lease.models import Proposal, Trade, Customer, Vehicle, Service
from app_lease.test.generator import random_proposal, random_customer
from django.contrib.auth.models import User


@pytest.mark.order(9)
@pytest.mark.django_db
def test_create_proposal():
    """ Creating proposal also creates related trade, vehicle, customer, service, user """

    # proposal object created
    created_proposal = random_proposal()
    assert True if isinstance(created_proposal, Proposal) else False

    # related records created
    assert True if User.objects.all().count() == 1 else False
    assert True if Customer.objects.all().count() == 1 else False
    assert True if Vehicle.objects.all().count() == 1 else False
    assert True if Service.objects.all().count() == 1 else False
    assert True if Trade.objects.all().count() == 1 else False
    assert True if Proposal.objects.all().count() == 1 else False

    # related records linked
    created_user = User.objects.first()
    created_customer = Customer.objects.first()
    created_vehicle = Vehicle.objects.first()
    created_service = Service.objects.first()
    created_trade = Trade.objects.first()
    assert True if created_proposal.trade == created_trade else False
    assert True if created_proposal.trade.service == created_service else False
    assert True if created_proposal.trade.vehicle == created_vehicle else False
    assert True if created_proposal.trade.vehicle.customer == created_customer else False
    assert True if created_proposal.trade.vehicle.customer.user == created_user else False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_delete_proposal():
    """ Delete proposal doesn't delete anything else """

    created_proposal = random_proposal()
    created_proposal.delete()

    assert True if User.objects.all().count() == 1 else False
    assert True if Customer.objects.all().count() == 1 else False
    assert True if Vehicle.objects.all().count() == 1 else False
    assert True if Service.objects.all().count() == 1 else False
    assert True if Trade.objects.all().count() == 1 else False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_delete_proposal_from_trade():
    """ Deleting trade must delete proposal """

    created_proposal = random_proposal()
    created_proposal.trade.delete()

    assert True if Proposal.objects.all().count() == 0 else False
    assert True if Trade.objects.all().count() == 0 else False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_delete_proposal_from_vehicle():
    """ Deleting vehicle must delete proposal """

    created_proposal = random_proposal()
    created_proposal.trade.vehicle.delete()

    assert True if Proposal.objects.all().count() == 0 else False
    assert True if Trade.objects.all().count() == 0 else False
    assert True if Vehicle.objects.all().count() == 0 else False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_delete_proposal_from_service():
    """ Deleting service must delete proposal """

    created_proposal = random_proposal()
    created_proposal.trade.service.delete()

    assert True if Proposal.objects.all().count() == 0 else False
    assert True if Trade.objects.all().count() == 0 else False
    assert True if Service.objects.all().count() == 0 else False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_delete_proposal_from_vehicle_customer():
    """ Deleting customer must delete proposal """

    created_proposal = random_proposal()
    created_proposal.trade.vehicle.customer.delete()

    assert True if Proposal.objects.all().count() == 0 else False
    assert True if Trade.objects.all().count() == 0 else False
    assert True if Vehicle.objects.all().count() == 0 else False
    assert True if Customer.objects.all().count() == 0 else False
    assert True if User.objects.all().count() == 0 else False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_delete_proposal_from_created_by_customer():
    """ Deleting customer that created the proposal must delete proposal """

    created_proposal = random_proposal()
    created_proposal.created_by_customer = random_customer()
    created_proposal.save()
    created_proposal.created_by_customer.save()
    created_proposal.created_by_customer.delete()

    assert True if Proposal.objects.all().count() == 0 else False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_delete_proposal_from_accepted_by_customer():
    """ Deleting customer that accepted the proposal must delete proposal """

    created_proposal = random_proposal()
    created_proposal.accepted_by_customer = random_customer()
    created_proposal.save()
    created_proposal.accepted_by_customer.save()
    created_proposal.accepted_by_customer.delete()

    assert True if Proposal.objects.all().count() == 0 else False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_custom_proposal():
    """ Test simple custom methods in proposal """

    created_proposal = random_proposal()
    assert True if isinstance(str(created_proposal), str) else False  # object returns valid string
    assert True if isinstance(created_proposal.proposed_by, str) else False  # returns valid str
    assert True if isinstance(created_proposal.monthly_payment, float) else False  # returns valid float
    assert True if isinstance(created_proposal.bi_weekly_payment, float) else False  # returns valid float
    assert True if isinstance(created_proposal.weekly_payment, float) else False  # returns valid float

    # try both with and without internal notes
    assert True if isinstance(created_proposal.show_notes, str) else False  # returns valid str
    created_proposal.system_note = 'my_internal_note'
    assert True if isinstance(created_proposal.show_notes, str) else False  # returns valid str


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
    created_proposal1.accept_proposal(created_customer2)

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
    created_proposal3.accept_proposal(owner)

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
    created_proposal2.refuse_proposal()

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
    created_proposal.cancel_proposal()

    # refresh model from database
    created_proposal.refresh_from_db()

    # check proposal was canceled
    assert True if created_proposal._status == 5 else False
    assert True if isinstance(created_proposal.system_note, str) else False  # note after canceling


# all tests for refuse proposal