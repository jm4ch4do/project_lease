import pytest
from app_lease.services.proposal_serv import accept_proposal
from app_lease.services.invoice_serv import pay_invoice
from app_lease.models import Invoice, Payment
from app_lease.test.generator import random_invoice, random_trade, random_service, \
    random_proposal, random_customer, random_creditcard


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
    accept_proposal(created_proposal, created_customer)

    # a new invoice is created
    assert True if Invoice.objects.all().count() == 1 else False

    # the new invoice is for the created trade and the vehicle owner
    created_invoice = Invoice.objects.all().first()
    assert True if created_invoice.trade == created_trade else False
    assert True if created_invoice.customer == created_trade.vehicle.customer else False


@pytest.mark.order(10)
@pytest.mark.django_db
def test_paying_invoice():
    """ Invoice can be paid using a credit card """

    created_invoice = random_invoice()
    created_customer = created_invoice.customer
    created_creditcard = random_creditcard(customer=created_customer)
    pay_invoice(created_invoice, created_creditcard)

    assert True if Payment.objects.all().count() == 1 else False
    assert True if Payment.objects.first().invoice == created_invoice else False
    assert True if Payment.objects.first().creditcard == created_creditcard else False
