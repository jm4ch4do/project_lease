from django.db import models
from .customer import Customer
from django.core.validators import RegexValidator
from ..validators import at_least_one_required


class Contact(models.Model):

    # foreign keys
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # string fields
    phone_number_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(validators=[phone_number_regex], max_length=16, unique=True,
                             blank=True, null=True, default="")
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True, default="")

    # flags
    CHOICES_TYPE_CONTACT = (
        (1, 'email'),
        (2, 'phone')
    )
    type = models.SmallIntegerField(choices=CHOICES_TYPE_CONTACT)

    # internal fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ordering
    class Meta:
        ordering = ['created_at']

    # validation
    def clean(self):

        # must provide at least one email or phone
        at_least_one_required([self.email, self.phone], 'email/phone')

    # string output
    def __str__(self):
        return self.customer.name + " (" + self.get_type_display() + ")"

