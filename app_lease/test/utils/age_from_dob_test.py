import pytest
from faker import Faker
from datetime import datetime
from app_lease.utils.age_from_dob import age_from_dob


@pytest.mark.django_db
def test_utils_age_from_dob():

    """ Testing function age_from_dob from the utils folder """
    fake = Faker()
    dob = fake.date_between(start_date=datetime(1950, 1, 1), end_date=datetime(2003, 1, 1)),
    age = age_from_dob(dob[0])
    assert True if isinstance(age, int) else False
