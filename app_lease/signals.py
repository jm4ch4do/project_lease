from django.dispatch import receiver
from django.db.models.signals import post_delete, post_init
from app_lease.models import Customer, Trade, Invoice
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError

# When a Customer is deleted, we should also delete the related User
@receiver(post_delete, sender=Customer)
def customer_delete_handler(sender, instance, *args, **kwargs):
    user_id = instance.user.id
    User.objects.get(pk=user_id).delete()
