from django.contrib import admin
from .models import customer, contact, lead

admin.site.register(customer.Customer)
admin.site.register(contact.Contact)
admin.site.register(lead.Lead)


