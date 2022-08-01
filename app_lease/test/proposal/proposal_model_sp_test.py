# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from django.db import IntegrityError
from app_lease.test.generator import random_proposal, random_customer
from django.core.exceptions import ValidationError
from datetime import date


@pytest.mark.order(9)
@pytest.mark.django_db
def test_empty_trade_in_proposal():
    """ A proposal can't have empty trade """

    created_proposal = random_proposal()
    try:
        created_proposal.trade = None
        created_proposal.save()  # modify proposal to have no related trade
    except IntegrityError as ex:
        assert True  # it should trigger an Exception
    else:
        assert False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_empty_created_by_customer_in_proposal():
    """ A proposal can't have empty created_by_customer """

    created_proposal = random_proposal()
    try:
        created_proposal.created_by_customer = None
        created_proposal.save()  # modify proposal to have no related trade
    except IntegrityError as ex:
        assert True  # it should trigger an Exception
    else:
        assert False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_not_equal_created_by_accepted_by_in_proposal():
    """ The fields created_by_customer and accepted_by_customer
        can't have the same customer """

    created_proposal = random_proposal()
    try:
        created_proposal.accepted_by_customer = created_proposal.created_by_customer
        created_proposal.full_clean()  # modify proposal to have no related trade
    except ValidationError as ex:
        assert True  # it should trigger an Exception
    else:
        assert False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_vehicle_owner_in_proposal():
    """ One of the  fields created_by_customer or accepted_by_customer
        must contain the owner of the car """

    created_proposal = random_proposal()
    created_customer1 = random_customer()
    created_customer2 = random_customer()

    try:
        created_proposal.accepted_by_customer = created_customer1
        created_proposal.created_by_customer = created_customer2
        created_proposal.full_clean()  # modify proposal to have no related trade
    except ValidationError as ex:
        assert True  # it should trigger an Exception
    else:
        assert False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_owner_out_of_proposal():
    """ Owner can't be left out of the proposal. He must be the creator
        or the one accepting the proposal.
    """

    # two customers come to shop
    created_customer2 = random_customer()
    created_customer3 = random_customer()

    # owner makes a proposals
    created_proposal1 = random_proposal()
    owner = created_proposal1.trade.vehicle.customer

    # customer2 makes another proposal
    created_proposal2 = random_proposal(trade=created_proposal1.trade, created_by_customer=created_customer2)

    # customer3 accepts customer 2 proposal which must result into an error
    with pytest.raises(ValidationError) as exp:
        created_proposal2.accept_proposal(created_customer3)
        created_proposal2.full_clean()
    assert True if exp else False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_owner_refuses_own_proposal():
    """ Owner can't refuse his own proposal """

    # owner makes a proposal
    created_proposal = random_proposal()

    # owner refuses his own proposal
    with pytest.raises(ValidationError) as exp:
        created_proposal.refuse_proposal()
        created_proposal.full_clean()
    assert True if exp else False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_owner_canceling_customer_proposal():
    """ Owner can't cancel some other customer's proposal """

    # one customer comes to shop
    created_customer2 = random_customer()

    # owner makes a proposal
    created_proposal = random_proposal()

    # customer2 makes another proposal
    created_proposal2 = random_proposal(trade=created_proposal.trade, created_by_customer=created_customer2)

    # owner cancel customer2's proposal -> triggers exception
    with pytest.raises(ValidationError) as exp:
        created_proposal2.cancel_proposal()
        created_proposal.full_clean()
    assert True if exp else False
