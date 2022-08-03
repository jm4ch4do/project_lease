import pytest
from app_lease.test.generator import random_trade, random_service, random_vehicle
from app_lease.models import Invoice
from app_lease.services.trade_serv import create_trade


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
