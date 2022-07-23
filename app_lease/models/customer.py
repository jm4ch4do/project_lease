from django.db import models
from django.contrib.auth.models import User
from app_lease.utils.age_from_dob import age_from_dob


class Customer(models.Model):

    # foreign keys
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # text fields
    first_name = models.CharField(blank=False, max_length=200)
    last_name = models.CharField(blank=False, max_length=200)
    job = models.CharField(blank=False, max_length=200)
    notes = models.TextField(blank=True, null=True, max_length=200)

    # date fields
    dob = models.DateField(blank=False)

    # flags
    CHOICES_CUSTOMER_STATUS = (
        (1, 'Active'),
        (2, 'Inactive')
    )
    status = models.SmallIntegerField(choices=CHOICES_CUSTOMER_STATUS)

    # internal fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # calculations
    @property
    def age(self):

        if not self.dob:
            return 0
        else:
            return age_from_dob(self.dob)

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    # ordering
    class Meta:
        ordering = ['first_name']

    # string output
    def __str__(self):
        return self.name
