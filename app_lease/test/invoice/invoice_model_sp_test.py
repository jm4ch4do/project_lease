import pytest
from django.db import IntegrityError
from app_lease.test.generator import random_invoice
from django.core.exceptions import ValidationError
from datetime import date


@pytest.mark.order(10)
@pytest.mark.django_db
def test_empty_trade_in_invoice():
    """ An invoice should not allow having no related trade """

    created_invoice = random_invoice()

    with pytest.raises(IntegrityError) as exp:
        created_invoice.trade = None
        created_invoice.save()
    assert True if exp else False


@pytest.mark.order(10)
@pytest.mark.django_db
def test_empty_customer_in_invoice():
    """ An invoice should not allow having no related customer """

    created_invoice = random_invoice()

    with pytest.raises(IntegrityError) as exp:
        created_invoice.customer = None
        created_invoice.save()
    assert True if exp else False
