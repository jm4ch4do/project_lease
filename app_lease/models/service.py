from django.db import models
from ..utils.age_from_dob import age_from_dob


class Lead(models.Model):

    # text fields
    first_name = models.CharField(blank=False, max_length=200)
    last_name = models.CharField(blank=False, max_length=200)
    source = models.URLField(blank=False, max_length=500)
    notes = models.TextField(blank=True, null=True, max_length=200)

    # date fields
    dob = models.DateField(blank=True, null=True)

    # internal fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # calculations
    @property
    def age(self):

        if not self.dob:
            None
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

