# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from app_lease.models import Proposal, Trade, Customer, Vehicle, Service
from app_lease.test.generator import random_proposal
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
    assert True if isinstance(created_proposal.show_notes, str) else False # returns valid str



# need method for accepting proposal where you can pass the customer accepting the proposal
# and it will change the status the accepted and leave a system_note
# accepting a proposal, closes other proposals in the same trade and accepts trade


# delete proposal deletes nothing else
# deleting trade, vehicle, service, customer or user deletes proposal


#  proposal can't have empty trade
#  proposal can't have empty created_by_customer


#  need method for canceling trade

# need to accept, close, cancel some proposals and trades in create_data command