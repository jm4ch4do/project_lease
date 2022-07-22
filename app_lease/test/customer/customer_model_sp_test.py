# ------------------------------ CUSTOMER MODEL HAPPY PATH ------------------------------
import pytest
from django.db import IntegrityError
from app_lease.test.utils import random_customer
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_empty_user_in_customer():
    """ A customer should not allow having no related user """

    created_customer = random_customer()
    try:
        created_customer.user = None
        created_customer.save()  # modify customer to have no related user
    except IntegrityError as ex:
        assert True  # it should trigger an Exception
    else:
        assert False


@pytest.mark.django_db
def test_string_user_in_customer():
    """ A customer should not allow having a string value as related user """

    created_customer = random_customer()
    try:
        created_customer.user = "related_user"
        created_customer.save()  # modify customer to have a string as related user
    except ValueError as ex:
        assert True  # it should trigger an Exception
    else:
        assert False


@pytest.mark.django_db
def test_none_fields_in_customer():
    """ A customer's first name can't be None """

    # customer should prevent first_name = None
    created_customer = random_customer()
    try:
        created_customer.first_name = None
        created_customer.save()
    except IntegrityError as ex:
        assert True  # it should trigger an Exception
    else:
        assert False


@pytest.mark.django_db
def test_blank_fields_customer():
    """ Several fields cannot be blank in customer """

    # first_name
    created_customer = random_customer()
    try:
        created_customer.first_name = ""
        created_customer.full_clean()  # run validation
    except ValidationError as ex:
        assert True  # it should trigger an Exception
    else:
        assert False

    # last_name
    created_customer = random_customer()
    with pytest.raises(ValidationError) as exp:
        created_customer.last_name = ""
        created_customer.full_clean()  # run validation
    assert True if exp else False

    # job
    created_customer = random_customer()
    with pytest.raises(ValidationError) as exp:
        created_customer.job = ""
        created_customer.full_clean()  # run validation
    assert True if exp else False

    # dob
    created_customer = random_customer()
    with pytest.raises(ValidationError) as exp:
        created_customer.dob = ""
        created_customer.full_clean()  # run validation
    assert True if exp else False
