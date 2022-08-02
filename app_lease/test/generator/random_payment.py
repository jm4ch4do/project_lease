from faker import Faker
from app_lease.test.generator import random_creditcard, random_invoice
from app_lease.utils.fake_provider import Provider
from app_lease.models import Payment
from datetime import datetime


def random_payment(total=1, creditcard=None, invoice=None, amount=None):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # ----- create payments
    created_payments = []
    for _ in range(total):

        # create invoice if needed
        created_invoice = random_invoice() if not invoice else invoice

        # create creditcard if needed
        created_creditcard = random_creditcard() if not creditcard else random_creditcard()

        # pay full amount if not specified
        selected_amount = amount if amount else created_invoice.amount

        # create payment
        created_payment = Payment.objects.create(
            creditcard=created_creditcard,
            invoice=created_invoice,
            amount=selected_amount,
        )

        created_payments.append(created_payment)

    if len(created_payments) == 1:
        return created_payment
    else:
        return created_payments
