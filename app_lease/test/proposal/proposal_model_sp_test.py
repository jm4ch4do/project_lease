# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from django.db import IntegrityError
from app_lease.test.generator import random_proposal
from django.core.exceptions import ValidationError
from datetime import date


@pytest.mark.order(9)
@pytest.mark.django_db
def test_empty_trade_in_proposal():
    """ A proposal can't have empty trade """

    created_proposal = random_proposal()
    try:
        created_proposal.trade = None
        created_proposal.save()  # modify proposal to have no related trade
    except IntegrityError as ex:
        assert True  # it should trigger an Exception
    else:
        assert False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_empty_created_by_customer_in_proposal():
    """ A proposal can't have empty created_by_customer """

    created_proposal = random_proposal()
    try:
        created_proposal.created_by_customer = None
        created_proposal.save()  # modify proposal to have no related trade
    except IntegrityError as ex:
        assert True  # it should trigger an Exception
    else:
        assert False


@pytest.mark.order(9)
@pytest.mark.django_db
def test_not_equal_created_by_accepted_by_in_proposal():
    """ The fields created_by_customer and accepted_by_customer
        can't have the same customer """

    created_proposal = random_proposal()
    try:
        created_proposal.accepted_by_customer = created_proposal.created_by_customer
        created_proposal.full_clean()  # modify proposal to have no related trade
    except ValidationError as ex:
        assert True  # it should trigger an Exception
    else:
        assert False

# also, one of them must be the owner of the car



# need method for accepting proposal where you can pass the customer accepting the proposal
# and it will change the status the accepted and leave a system_note
# accepting a proposal, closes other proposals in the same trade and accepts trade



#  need method for canceling trade

# need to accept, close, cancel some proposals and trades in create_data command