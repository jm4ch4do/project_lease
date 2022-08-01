from django.db import models


class Service(models.Model):

    # text fields
    name = models.CharField(blank=False, max_length=200)
    cost = models.FloatField(blank=False, max_length=200)
    description = models.TextField(blank=True, null=True, max_length=500)

    WHEN_TO_PAY_CHOICES_SERVICE = (
        (1, 'Start'),
        (2, 'End')
    )
    when_to_pay = models.SmallIntegerField(choices=WHEN_TO_PAY_CHOICES_SERVICE)

    TYPE_CHOICES_SERVICE = (
        (1, 'Lease'),
        (2, 'Sale')
    )
    service_type = models.SmallIntegerField(choices=TYPE_CHOICES_SERVICE)

    # internal fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # calculation
    @property
    def label(self):
        return self.name + " (" + str(self.cost) + ")"

    # ordering
    class Meta:
        ordering = ['service_type', 'name']

    # string output
    def __str__(self):
        return self.label
