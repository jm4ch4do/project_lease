from django.db import models
from ..models import Customer


class Vehicle(models.Model):

    # foreign keys
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # text fields for vehicle
    make_model = models.CharField(blank=False, max_length=200)
    make = models.CharField(blank=False, max_length=200)
    model = models.CharField(blank=False, max_length=200)
    category = models.CharField(blank=False, max_length=200)
    machine_make_model = models.CharField(blank=True, null=True, max_length=200)
    machine_make = models.CharField(blank=True, null=True, max_length=200)
    machine_model = models.CharField(blank=True, null=True, max_length=200)
    machine_category = models.CharField(blank=True, null=True, max_length=200)

    # numeric fields
    year = models.PositiveSmallIntegerField(blank=False)
    machine_year = models.PositiveSmallIntegerField(blank=True, null=True)

    # internal fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # calculations
    @property
    def name(self):
        return " ".join((
            str(self.year), self.make, self.model, "(" + self.category + ")"
        ))

    # ordering
    class Meta:
        ordering = ['year', 'make']

    # string output
    def __str__(self):
        return self.name

