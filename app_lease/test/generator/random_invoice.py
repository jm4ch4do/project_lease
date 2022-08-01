from faker import Faker
from app_lease.test.generator import random_trade, random_customer
from app_lease.utils.fake_provider import Provider
from app_lease.models import Invoice
from datetime import datetime


def random_invoice(total=1, trade=None, customer=None, amount=None):

    # register custom functions
    fake = Faker()
    fake.add_provider(Provider)

    # ----- create invoices
    created_invoices = []
    for _ in range(total):

        # create trade if needed
        created_trade = random_trade() if not trade else trade

        # create customer if needed
        created_customer = random_customer() if not customer else customer

        # get amount from service if not provided
        selected_amount = created_trade.service.cost if not amount else amount

        # create invoice
        created_invoice = Invoice.objects.create(
            trade=created_trade,
            customer=created_customer,
            amount=selected_amount,
        )

        created_invoices.append(created_invoice)

    if len(created_invoices) == 1:
        return created_invoice
    else:
        return created_invoices
