from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('RETAIL', 'Retail Customer'),
        ('WHOLESALE', 'Wholesale Client'),
        ('ADMIN', 'Store Admin'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='RETAIL')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    is_approved_wholesale = models.BooleanField(default=False)

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    base_retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    base_wholesale_price = models.DecimalField(max_digits=10, decimal_places=2)
    tech_pack_url = models.URLField(blank=True, null=True) # For B2B downloads
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    size = models.CharField(max_length=50) # e.g., OS, S, M, L, XL
    color = models.CharField(max_length=50)
    sku = models.CharField(max_length=100, unique=True)
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} - {self.size}/{self.color}"

class TieredPricingRule(models.Model):
    """Dynamic pricing logic for wholesale accounts based on volume."""
    product = models.ForeignKey(Product, related_name='pricing_tiers', on_delete=models.CASCADE)
    min_quantity = models.PositiveIntegerField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2) # e.g., 20.00 for 20% off

    def __str__(self):
        return f"{self.product.title} - {self.min_quantity}+ ({self.discount_percentage}%)"

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Payment'),
        ('PAID', 'Paid'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_wholesale_order = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.variant.product.title}"
