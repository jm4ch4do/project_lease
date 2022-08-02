from django.db import models
from .customer import Customer
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator

class CreditCard(models.Model):

    # foreign keys
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)

    # string fields
    name_in_card = models.CharField(blank=False, max_length=200)
    provider = models.CharField(blank=False, max_length=200)

    # numeric fields
    expire_month = models.IntegerField(blank=False, validators=[
        MaxValueValidator(12), MinValueValidator(1)
    ])

    expire_year = models.IntegerField(blank=False, validators=[
        MaxValueValidator(datetime.today().year - 10), MinValueValidator(datetime.today().year + 20)
    ])
    security_code = models.IntegerField(blank=False, validators=[
        MaxValueValidator(999), MinValueValidator(100)
    ])
    card_number = models.BigIntegerField(blank=False, validators=[
        MinLengthValidator(12), MaxLengthValidator(19)
    ])

    # calculations
    @property
    def is_active(self):

        if self.expire_year > datetime.today().year:
            return True

        elif self.expire_year == datetime.today().year:
            if self.expire_month >= datetime.today().month:
                return True

        else:
            return False

    @property
    def label(self):
        return self.name_in_card + ' (' + self.provider + ' )' + ' ........' + str(self.card_number)[-4:]

    # string output
    def __str__(self):
        return self.label
