from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from app_lease.models import Customer, Trade, Invoice
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.conf import settings
from rest_framework.authtoken.models import Token


# When a Customer is deleted, we should also delete the related User
@receiver(post_delete, sender=Customer)
def customer_delete_handler(sender, instance, *args, **kwargs):
    user_id = instance.user.id
    User.objects.get(pk=user_id).delete()


# every time a user is created a token will be generated
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
