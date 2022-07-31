# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from app_lease.models import Invoice, Customer, Vehicle, Service, Trade
from app_lease.test.generator import random_invoice, random_trade, random_service, random_proposal, random_customer
from django.contrib.auth.models import User

# creating invoice creates, trade, vehicle, service, customer, user


@pytest.mark.order(10)
@pytest.mark.django_db(transaction=True)
def test_create_invoice():
    """ Creating invoice also creates related trade and customer """

    # invoice object created
    created_invoice = random_invoice()
    assert True if isinstance(created_invoice, Invoice) else False

    # related records created
    assert True if User.objects.all().count() == 2 else False
    assert True if Customer.objects.all().count() == 2 else False
    assert True if Vehicle.objects.all().count() == 1 else False
    assert True if Service.objects.all().count() == 1 else False
    assert True if Trade.objects.all().count() == 1 else False


@pytest.mark.order(10)
@pytest.mark.django_db
def test_delete_invoice():
    """ Delete invoice deletes nothing else"""

    # create and delete invoice
    created_invoice = random_invoice()
    Invoice.objects.all().delete()
    assert True if Invoice.objects.all().count() == 0 else False

    # no other records deleted
    assert True if User.objects.all().count() == 2 else False
    assert True if Customer.objects.all().count() == 2 else False
    assert True if Vehicle.objects.all().count() == 1 else False
    assert True if Service.objects.all().count() == 1 else False
    assert True if Trade.objects.all().count() == 1 else False


@pytest.mark.order(10)
@pytest.mark.django_db
def test_delete_invoice_from_trade():
    """ Deleting trade must delete invoice """

    created_invoice = random_invoice()
    created_invoice.trade.delete()

    assert True if Invoice.objects.all().count() == 0 else False
    assert True if Trade.objects.all().count() == 0 else False


@pytest.mark.order(10)
@pytest.mark.django_db
def test_delete_invoice_from_customer():
    """ Deleting customer must delete invoice """

    created_invoice = random_invoice()
    created_invoice.customer.delete()

    assert True if Invoice.objects.all().count() == 0 else False
    assert True if Customer.objects.all().count() == 1 else False  # two customer were created for invoice


@pytest.mark.order(10)
@pytest.mark.django_db
def test_create_invoice_from_trade():
    """ An invoice must be created when accepting a proposal type sale """

    # customer comes to store
    created_customer = random_customer()

    # owner proposes a sale
    created_service = random_service(service_type=2)
    created_trade = random_trade(service=created_service)
    created_proposal = random_proposal(trade=created_trade)

    # customer accepts proposal
    created_proposal.accept_proposal(created_customer)

    # a new invoice is created
    assert True if Invoice.objects.all().count() == 1 else False

    # the new invoice is for the created trade and the vehicle owner
    created_invoice = Invoice.objects.all().first()
    assert True if created_invoice.trade == created_trade else False
    assert True if created_invoice.customer == created_trade.vehicle.customer else False


@pytest.mark.order(10)
@pytest.mark.django_db
def test_custom_invoice():
    """ Test custom methods in invoice """

    created_invoice = random_invoice()
    assert True if isinstance(str(random_invoice), str) else False
    assert True if isinstance(created_invoice.label, str) else False
    assert True if isinstance(created_invoice.days_remaining, int) else False
