from django.contrib import admin
from .models import Customer, Contact, Lead, Vehicle, Service, Trade,\
    Proposal, Invoice, CreditCard, Payment

admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(Lead)
admin.site.register(Vehicle)
admin.site.register(Service)
admin.site.register(Trade)
admin.site.register(Proposal)
admin.site.register(Invoice)
admin.site.register(CreditCard)
admin.site.register(Payment)
