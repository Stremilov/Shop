from shopapp.models import Order

from django.core.management import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Creating order')
        user = User.objects.get(username='admin')
        order = Order.objects.get_or_create(
            delivery_adress='Main street, h.8',
            promocode='shop322',
            user=user,
        )
        self.stdout.write(self.style.SUCCESS(f'created order {order}'))
