from django.db import models
from customer import Customer


class Contact(models.Model):

    # foreign keys
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
