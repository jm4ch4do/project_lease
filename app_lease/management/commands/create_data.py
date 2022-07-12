from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Command Information"

    def handle(self, *args, **kwargs):
        print("hello")