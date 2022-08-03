import pytest
from app_lease.test.generator import random_proposal, random_customer, random_service, random_vehicle
from app_lease.models import Invoice
from app_lease.services.trade_serv import create_trade, cancel_trade


@pytest.mark.order(8)
@pytest.mark.django_db
def test_create_trade_and_related_invoice_for_type_lease():
    """ When creating a trade, an invoice must also be created if the
        trade's service is type = lease
     """

    # a trade is created for a service type Lease
    created_service = random_service(service_type=1)
    created_vehicle = random_vehicle()
    created_trade = create_trade(service=created_service, vehicle=created_vehicle)

    # verify it created an invoice
    assert True if Invoice.objects.all().count() == 1 else False
    created_invoice = Invoice.objects.first()
    assert True if created_invoice.trade == created_trade else False
    assert True if created_invoice.trade.service == created_service else False
    assert True if created_invoice.amount == created_service.cost else False


@pytest.mark.order(8)
@pytest.mark.django_db
def test_cancel_trade():
    """ Canceling a trade closes related proposals """

    # two customers come to shop
    created_customer2 = random_customer()
    created_customer3 = random_customer()

    # owner makes a proposal
    created_proposal1 = random_proposal()
    owner = created_proposal1.trade.vehicle.customer

    # customer2 and customer3 make two proposals
    created_proposal2 = random_proposal(trade=created_proposal1.trade, created_by_customer=created_customer2)
    created_proposal3 = random_proposal(trade=created_proposal1.trade, created_by_customer=created_customer3)

    # trade is canceled
    cancel_trade(created_proposal1.trade)

    # refresh model from database
    created_proposal1.refresh_from_db(), created_proposal2.refresh_from_db(), created_proposal3.refresh_from_db()

    # ----- results
    # trade is canceled and proposals are closed
    assert True if created_proposal1.trade.status == 3 else False
    assert True if created_proposal1._status == 4 else False
    assert True if created_proposal2._status == 4 else False
    assert True if created_proposal3._status == 4 else False
    assert True if isinstance(created_proposal1.system_note, str) else False
    assert True if isinstance(created_proposal2.system_note, str) else False
    assert True if isinstance(created_proposal3.system_note, str) else False