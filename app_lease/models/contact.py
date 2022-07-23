from django.db import models
from .customer import Customer
from .lead import Lead
from django.core.validators import RegexValidator
from ..validators import at_least_one_required


class Contact(models.Model):

    # foreign keys
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, null=True, blank=True, on_delete=models.CASCADE)

    # string fields
    phone_number_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(validators=[phone_number_regex], max_length=16,
                             blank=True, null=True, default="")
    email = models.EmailField(max_length=254, blank=True, null=True, default="")
    note = models.CharField(blank=True, null=True, max_length=200)

    # flags
    CHOICES_CONTACT_TYPE = (
        (1, 'email'),
        (2, 'phone')
    )
    type = models.SmallIntegerField(choices=CHOICES_CONTACT_TYPE)

    # internal fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ordering
    class Meta:
        ordering = ['customer__first_name']

    # validation
    def clean(self):

        # must provide at least one email or phone
        at_least_one_required([self.email, self.phone], 'email/phone')
        at_least_one_required([self.customer, self.lead], 'customer/lead')

    # string output
    def __str__(self):

        if self.customer:
            name = self.customer.name

        elif self.lead:
            name = self.lead.name

        else:
            name = 'unknown'

        return name + " (" + self.get_type_display() + ")"

