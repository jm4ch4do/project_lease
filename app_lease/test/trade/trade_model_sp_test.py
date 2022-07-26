import pytest
from app_lease.models import Customer
from app_lease.test.generator import random_trade
from django.contrib.auth.models import User
from django.db import IntegrityError


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
