from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Customer(models.Model):

    # foreign keys
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # text fields
    first_name = models.CharField(blank=False, max_length=200)
    last_name = models.CharField(blank=False, max_length=200)
    notes = models.TextField(blank=True, null=True, max_length=200)

    # date fields
    dob = models.DateField(blank=False)

    # flags
    CHOICES_CUSTOMER_STATUS = (
        (0, 'Active'),
        (1, 'Inactive')
    )
    status = models.SmallIntegerField(choices=CHOICES_CUSTOMER_STATUS)

    # internal fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.PositiveIntegerField(blank=True, null=True)
    updated_by = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    # calculations
    @property
    def age(self):
        today = date.today()
        dob = self.dob
        diff_in_years = today.year - dob.year

        if today.month < dob.month:
            has_birthday_passed = False
        elif today.month > dob.month:
            has_birthday_passed = True
        elif today.day >= dob.day:
            has_birthday_passed = True
        else:
            has_birthday_passed = False

        age = diff_in_years if has_birthday_passed else diff_in_years - 1

        return age

    @property
    def name(self):
        return self.first_name + " " + self.last_name
