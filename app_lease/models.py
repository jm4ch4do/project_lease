from django.db import models
from django.contrib.auth.models import User


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
    created_by = models.PositiveIntegerField()
    updated_by = models.PositiveIntegerField()

