from django.dispatch import receiver
from django.db.models.signals import post_delete, post_init
from app_lease.models import Customer, Trade, Invoice
from django.contrib.auth.models import User


# When a Customer is deleted, we should also delete the related User
@receiver(post_delete, sender=Customer)
def customer_delete_handler(sender, instance, *args, **kwargs):
    user_id = instance.user.id
    User.objects.get(pk=user_id).delete()


# When a trade is created, a proposal should also be created is trade is lease
# @receiver(post_init, sender=Trade)
# def trade_create_handler(sender, instance, *args, **kwargs):
#     created_trade = instance
#
#     if created_trade.service.service_type == 1:
#         # create invoice
#         Invoice.objects.create(
#             trade=created_trade,
#             customer=created_trade.vehicle.customer,
#             amount=created_trade.service.cost,
#             system_note='for accepting proposal for service sale'
#         )



