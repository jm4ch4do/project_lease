from random import randint
from django.contrib.auth.models import User
import pytest

@pytest.mark.django_db
def test_home_view():

    while 1:
        username = 'pepe'.lower() + str(randint(1, 999999))
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            break