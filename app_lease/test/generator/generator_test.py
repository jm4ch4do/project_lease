from django.contrib.auth.models import User
from app_lease.test.generator import *
from app_lease.models import *
import pytest


@pytest.mark.order(1)
@pytest.mark.django_db
def test_random_contact():

    print('testing contact')
    created_contact = random_contact()
    assert True if isinstance(created_contact, Contact) else False


@pytest.mark.order(1)
@pytest.mark.django_db
def test_random_customer():

    print('testing customer')
    created_customer = random_customer()
    assert True if isinstance(created_customer, Customer) else False


@pytest.mark.order(1)
@pytest.mark.django_db
def test_random_lead():

    created_lead = random_lead()
    assert True if isinstance(created_lead, Lead) else False


@pytest.mark.order(1)
@pytest.mark.django_db
def test_random_service():

    created_service = random_service()
    assert True if isinstance(created_service, Service) else False


@pytest.mark.order(1)
@pytest.mark.django_db
def test_random_user():

    created_user = random_user()
    assert True if isinstance(created_user, User) else False


@pytest.mark.order(1)
@pytest.mark.django_db
def test_random_vehicle():

    created_vehicle = random_vehicle()
    assert True if isinstance(created_vehicle, Vehicle) else False


@pytest.mark.order(1)
@pytest.mark.django_db
def test_random_trade():

    created_trade = random_trade()
    assert True if isinstance(created_trade, Trade) else False


@pytest.mark.order(1)
@pytest.mark.django_db
def test_random_proposal():

    created_proposal = random_proposal()
    assert True if isinstance(created_proposal, Proposal) else False


@pytest.mark.order(1)
@pytest.mark.django_db
def test_random_invoice():

    created_invoice = random_invoice()
    assert True if isinstance(created_invoice, Invoice) else False


@pytest.mark.order(1)
@pytest.mark.django_db
def test_random_creditcard():

    created_creditcard = random_creditcard()
    assert True if isinstance(created_creditcard, CreditCard) else False
