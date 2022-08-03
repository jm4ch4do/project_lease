from app_lease.models import Payment
from django.core.exceptions import ValidationError


def pay_invoice(invoice, credit_card, payment_amount=None):

    # can't pay if there is nothing owed
    if invoice.left_to_pay == 0:
        raise ValidationError(
            "Can't paid because there is nothing owed",
            code='paying_already_paid_invoice'
        )

    # can't pay more than left_to_pay
    if payment_amount and payment_amount > invoice.left_to_pay:
        raise ValidationError(
            "Can't pay more than amount owed which is " + str(invoice.left_to_pay),
            code='overpaying_invoice'
        )

    # no amount specified to pay -> pay maximum
    payment_amount = invoice.left_to_pay if not payment_amount else payment_amount

    # create payment
    created_payment = Payment.objects.create(
        creditcard=credit_card,
        invoice=invoice,
        amount=payment_amount,
    )
