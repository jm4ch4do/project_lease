import pytest
from app_lease.models import Trade, Customer, Vehicle, Service
from app_lease.test.generator import random_trade
from django.contrib.auth.models import User


@pytest.mark.order(8)
@pytest.mark.django_db
def test_create_trade():
    """ Creating trade also creates related user service, vehicle, customer and user """

    # trade object created
    created_trade = random_trade()
    assert True if isinstance(created_trade, Trade) else False

    # related records created
    assert True if User.objects.all().count() == 1 else False
    assert True if Customer.objects.all().count() == 1 else False
    assert True if Vehicle.objects.all().count() == 1 else False
    assert True if Service.objects.all().count() == 1 else False
    assert True if Trade.objects.all().count() == 1 else False

    # related records linked
    created_user = User.objects.first()
    created_customer = Customer.objects.first()
    created_vehicle = Vehicle.objects.first()
    created_service = Service.objects.first()
    assert True if created_trade.service == created_service else False
    assert True if created_trade.vehicle == created_vehicle else False
    assert True if created_trade.vehicle.customer == created_customer else False
    assert True if created_trade.vehicle.customer.user == created_user else False


@pytest.mark.order(8)
@pytest.mark.django_db
def test_delete_trade():
    """ Delete trade doesn't delete anything else """

    created_trade = random_trade()
    created_trade.delete()

    assert True if User.objects.all().count() == 1 else False
    assert True if Customer.objects.all().count() == 1 else False
    assert True if Vehicle.objects.all().count() == 1 else False
    assert True if Service.objects.all().count() == 1 else False


@pytest.mark.order(8)
@pytest.mark.django_db
def test_delete_trade_from_service():
    """ Deleting service must delete trade """

    created_trade = random_trade()
    created_trade.service.delete()

    assert True if Service.objects.all().count() == 0 else False
    assert True if Trade.objects.all().count() == 0 else False


@pytest.mark.order(8)
@pytest.mark.django_db
def test_delete_trade_from_vehicle():
    """ Deleting vehicle must delete trade """

    created_trade = random_trade()
    created_trade.vehicle.delete()

    assert True if Vehicle.objects.all().count() == 0 else False
    assert True if Trade.objects.all().count() == 0 else False


@pytest.mark.order(8)
@pytest.mark.django_db
def test_delete_trade_from_customer():
    """ Deleting customer must delete trade """

    created_trade = random_trade()
    created_trade.vehicle.customer.delete()

    assert True if Customer.objects.all().count() == 0 else False
    assert True if Trade.objects.all().count() == 0 else False


@pytest.mark.order(8)
@pytest.mark.django_db
def test_delete_trade_from_user():
    """ Deleting user must delete trade """

    created_trade = random_trade()
    created_trade.vehicle.customer.user.delete()

    assert True if User.objects.all().count() == 0 else False
    assert True if Trade.objects.all().count() == 0 else False


@pytest.mark.order(8)
@pytest.mark.django_db
def test_custom_trade():
    """ Test custom methods in customer """

    created_trade = random_trade()
    assert True if isinstance(str(random_trade), str) else False  # object returns valid string
    assert True if isinstance(created_trade.label, str) else False  # label return valid str

