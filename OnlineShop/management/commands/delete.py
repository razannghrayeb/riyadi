from django.core.management.base import BaseCommand
from OnlineShop.models import Product, Category

class Command(BaseCommand):
    help = 'Cleans up duplicate products'

    def handle(self, *args, **options):
        # Option 1: Delete all products
        Product.objects.all().delete()
        print("All products have been deleted.")

        # Option 2: Delete specific duplicates or use conditions
        # This assumes you have a way to identify duplicates, e.g., by name
        products = Product.objects.all()
        seen = set()
        for product in products:
            if product.name in seen:
                product.delete()
            else:
                seen.add(product.name)
        print("Duplicate products have been cleaned up.")
