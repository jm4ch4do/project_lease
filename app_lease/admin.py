from django.contrib import admin
from .models import Customer, Contact, Lead, Vehicle, Service

admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(Lead)
admin.site.register(Vehicle)
admin.site.register(Service)
