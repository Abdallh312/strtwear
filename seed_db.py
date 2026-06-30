import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from store.models import Product, ProductVariant, TieredPricingRule

def seed():
    print("Clearing existing products...")
    Product.objects.all().delete()

    print("Creating products...")
    p1 = Product.objects.create(
        title='Heavyweight Hoodie',
        slug='heavyweight-hoodie',
        description='500gsm premium cotton hoodie.',
        base_retail_price=120.00,
        base_wholesale_price=60.00,
    )
    ProductVariant.objects.create(product=p1, size='L', color='Black', sku='HH-L-BLK', stock_quantity=100)
    TieredPricingRule.objects.create(product=p1, min_quantity=20, discount_percentage=20.00)

    p2 = Product.objects.create(
        title='Cargo Parachute Pants',
        slug='cargo-parachute-pants',
        description='Nylon blend with adjustable straps.',
        base_retail_price=150.00,
        base_wholesale_price=75.00,
    )
    ProductVariant.objects.create(product=p2, size='M', color='Olive', sku='CPP-M-OLV', stock_quantity=50)
    TieredPricingRule.objects.create(product=p2, min_quantity=20, discount_percentage=15.00)

    p3 = Product.objects.create(
        title='Graphic Box Tee',
        slug='graphic-box-tee',
        description='Acid wash oversized fit.',
        base_retail_price=45.00,
        base_wholesale_price=20.00,
    )
    ProductVariant.objects.create(product=p3, size='XL', color='Charcoal', sku='GBT-XL-CHR', stock_quantity=200)
    TieredPricingRule.objects.create(product=p3, min_quantity=50, discount_percentage=25.00)

    print("Database seeded successfully!")

if __name__ == '__main__':
    seed()
