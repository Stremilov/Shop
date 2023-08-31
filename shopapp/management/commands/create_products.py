from django.core.management import BaseCommand

from shopapp.models import Models


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Create products")

        products_names = [
            'laptop',
            'desktop',
            'phone',
        ]

        for products_name in products_names:
            product, created = Models.objects.get_or_create(name=products_name)
            self.stdout.write(f'Product {product.name} creating')
            self.stdout.write(self.style.SUCCESS(f'Product {product.name} created sucsessfully'))

        self.stdout.write(self.style.SUCCESS('Products created sucsessfully'))
