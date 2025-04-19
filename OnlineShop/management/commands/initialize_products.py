import os
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from OnlineShop.models import Product, Category  # Adjust the import path based on your app's structure

class Command(BaseCommand):
    help = 'Populates the database with product data'

    def handle(self, *args, **options):
        categories_data = ['Official Jerseys', 'Fan Collection', 'Scarves', 'Training Collection']
        for category_name in categories_data:
            Category.objects.get_or_create(name=category_name)

        products_data = [
            {'name': 'RBL NIKE AWAY JERSEY 23/24', 'description': 'Official away team jersey', 'price': 94.95, 'category': 'Official Jerseys', 'image_path': 'OnlineShop/static/pics/RBLZ-Jersey-23-24.jpg'},
            {'name': 'RBL NIKE HOME JERSEY 23/24', 'description': 'Official home team jersey', 'price': 94.95, 'category': 'Official Jerseys', 'image_path': 'OnlineShop/static/pics/RBL-Nike-Home-Jersey-23-24.jpg'},
            {'name': 'RBL NIKE THIRD JERSEY 23/24', 'description': 'Official third team jersey', 'price': 94.95, 'category': 'Official Jerseys', 'image_path': 'OnlineShop/static/pics/RBL-Nike-Third-Jersey-23-24.jpg'},
            {'name': 'RBL YOUTH JUMP BULLI T-SHIRT', 'description': 'RB Leipzig Bulli T-Shirt for youth', 'price': 19.95, 'category': 'Fan Collection', 'image_path': 'OnlineShop/static/pics/RBL-Youth-Jump.jpg'},
            {'name': 'DFB POKAL', 'description': 'Cup won in 2022 and 2023', 'price': 79.95, 'category': 'Fan Collection', 'image_path': 'OnlineShop/static/pics/pokal.jpg'},
            {'name': 'RBL Fan Beanie Navy', 'description': 'Hat with team colors and logo', 'price': 19.95, 'category': 'Fan Collection', 'image_path': 'OnlineShop/static/pics/cap.jpg'},
            {'name': 'RB Leipzig 2024 - Fanplanner', 'description': 'Fan plans for the year', 'price': 12.95, 'category': 'Fan Collection', 'image_path': 'OnlineShop/static/pics/RB-Leipzig-2024-Fanplanner.jpg'},
            {'name': 'RBL Simons Player Scarf', 'description': 'RB Leipzig Simons Player Scarf', 'price': 17.95, 'category': 'Scarves', 'image_path': 'OnlineShop/static/pics/simonsscarf.png'},
            {'name': 'RBL Winter Scarf 2023', 'description': 'RB Leipzig Winter Scarf', 'price': 17.95, 'category': 'Scarves', 'image_path': 'OnlineShop/static/pics/winterscarf.jpg'},
            {'name': 'RBL Dark Scarf', 'description': 'RB Leipzig dark Scarf', 'price': 18.95, 'category': 'Scarves', 'image_path': 'OnlineShop/static/pics/die roten.png'},
            {'name': 'RBL Blue Scarf', 'description': 'RB Leipzig blue scarf', 'price': 18.95, 'category': 'Fan Collection', 'image_path': 'OnlineShop/static/pics/picture14.jpg'},
            {'name': 'RBL Nike Pro Training Longsleeve 23/24', 'description': 'Pro Training Longsleeve for men by Nike', 'price': 64.95, 'category': 'Training Collection', 'image_path': 'OnlineShop/static/pics/jacket.jpg'},
            {'name': 'RBL Nike Leipzig T-Shirt 23/24', 'description': 'Leipzig T-Shirt for men by Nike', 'price': 34.95, 'category': 'Training Collection', 'image_path': 'OnlineShop/static/pics/leipzig nike.jpg'},
            {'name': 'RBL Nike Training Men T-Shirt 23/24', 'description': 'Leipzig T-Shirt for men by Nike', 'price': 44.95, 'category': 'Training Collection', 'image_path': 'OnlineShop/static/pics/training men.jpg'},
            {'name': 'RBL Nike Training Women T-Shirt 23/24', 'description': 'Training T-Shirt for women by Nike', 'price': 44.95, 'category': 'Training Collection', 'image_path': 'OnlineShop/static/pics/training woman.jpg'},
            {'name': 'RBL Nike Training Men Shorts 23/24', 'description': 'Training Shorts for men by Nike', 'price': 39.95, 'category': 'Training Collection', 'image_path': 'OnlineShop/static/pics/shortsmen.jpg'},
            {'name': 'RBL Nike Training Woman Shorts 23/24', 'description': 'Training Shorts for women by Nike', 'price': 39.95, 'category': 'Training Collection', 'image_path': 'OnlineShop/static/pics/shortswoman.jpg'},
            
        ]
        for product_data in products_data:
            category = Category.objects.get(name=product_data['category'])
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': category
                }
            )
            if product_data['image_path'] and created:
                image_path = os.path.join(product_data['image_path'])
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        product.image.save(os.path.basename(image_path), File(f), save=True)
        print("Products and categories initialized successfully.")