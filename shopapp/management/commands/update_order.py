from django.core.management import BaseCommand

from shopapp.models import Order, Models


class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            self.stdout.write('no orders found')
            return
        products = Models.objects.all()
        for product in products:
            order.products.add(product)

        order.save()
        self.stdout.write(
            self.style.SUCCESS(f'Succesfully added products {order.products.all()} to order {order}')
        )