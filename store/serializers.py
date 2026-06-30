from rest_framework import serializers
from .models import Product, ProductVariant, TieredPricingRule

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'color', 'sku', 'stock_quantity']

class TieredPricingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TieredPricingRule
        fields = ['min_quantity', 'discount_percentage']

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    pricing_tiers = TieredPricingRuleSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'description', 
            'base_retail_price', 'base_wholesale_price', 
            'tech_pack_url', 'is_active', 'variants', 'pricing_tiers'
        ]
