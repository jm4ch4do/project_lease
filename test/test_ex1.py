import pytest
from django.contrib.auth.models import User

@pytest.fixture
def user_1(db):
    return User.objects.create_user("test-user")

@pytest.mark.django_db
def test_set_check_password(user_1):
    assert user_1.username == "test-user"
