import pytest
from app_lease.test.generator import random_trade, random_customer, random_proposal
from django.db import IntegrityError
from django.core.exceptions import ValidationError


@pytest.mark.order(8)
@pytest.mark.django_db
def test_duplicated_vehicle_service_combination_in_trade():
    """ The combination of vehicle and service must be unique in trade table """

    created_trade1 = random_trade()
    service, vehicle = created_trade1.service, created_trade1.vehicle

    with pytest.raises(IntegrityError) as exp:
        random_trade(service=service, vehicle=vehicle)
        # created_trade2.save()
    assert True if exp else False


@pytest.mark.order(8)
@pytest.mark.django_db
def test_service_empty_in_trade():
    """ Service cannot be empty in trade table """

    created_trade = random_trade()

    with pytest.raises(IntegrityError) as exp:
        created_trade.service = None
        created_trade.save()
    assert True if exp else False


@pytest.mark.order(8)
@pytest.mark.django_db
def test_vehicle_empty_in_trade():
    """ Vehicle cannot be empty in trade table """

    created_trade = random_trade()

    with pytest.raises(IntegrityError) as exp:
        created_trade.vehicle = None
        created_trade.save()
    assert True if exp else False


@pytest.mark.order(8)
@pytest.mark.django_db
def test_status_not_empty_in_trade():
    """ The status of the trade can't be empty """

    created_trade = random_trade()

    with pytest.raises(ValidationError) as exp:
        created_trade.status = None
        created_trade.full_clean()
    assert True if exp else False


@pytest.mark.order(8)
@pytest.mark.django_db
def test_cant_cancel_accepted_trade():
    """ An accepted trade can't be canceled """

    # one customer comes to shop
    created_customer2 = random_customer()

    # owner makes a proposal
    created_proposal = random_proposal()

    # customer2 accepts proposal
    created_proposal.accept_proposal(created_customer2)

    # refresh model from database
    created_proposal.refresh_from_db()

    # trade can't be canceled because was previously accepted
    with pytest.raises(ValidationError) as exp:
        created_proposal.trade.cancel_trade()
    assert True if exp else False
