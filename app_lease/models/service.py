from django.db import models
from ..utils.age_from_dob import age_from_dob


class Service(models.Model):

    # text fields
    name = models.CharField(blank=False, max_length=200)
    cost = models.FloatField(blank=False, max_length=200)
    description = models.TextField(blank=True, null=True, max_length=500)

    SERVICE_TYPE = (
        (1, 'Lease'),
        (2, 'Sale')
    )
    type = models.SmallIntegerField(choices=SERVICE_TYPE)

    # internal fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def label(self):
        return self.name + " (" + str(self.cost) + ")"

    # ordering
    class Meta:
        ordering = ['type', 'name']

    # string output
    def __str__(self):
        return self.label
