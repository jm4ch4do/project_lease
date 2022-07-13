from django.contrib import admin
from .models import customer, contact

admin.site.register(customer.Customer)
admin.site.register(contact.Contact)


