import pytest
from pytest_factoryboy import register
from test.factories import UserFactory, CustomerFactory

register(UserFactory)
register(CustomerFactory)


@pytest.fixture
def new_user(db, user_factory):
    user = user_factory.create()
    return user


@pytest.fixture
def new_customer(db, customer_factory):
    customer = customer_factory.create()
    return customer

