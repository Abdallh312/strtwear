from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, ProductVariant, TieredPricingRule, Order, OrderItem

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'company_name', 'tax_id', 'is_approved_wholesale')}),
    )
    list_display = ('username', 'email', 'role', 'company_name', 'is_approved_wholesale', 'is_staff')
    list_filter = ('role', 'is_approved_wholesale', 'is_staff')
    search_fields = ('username', 'email', 'company_name')

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class TieredPricingRuleInline(admin.TabularInline):
    model = TieredPricingRule
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'base_retail_price', 'base_wholesale_price', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductVariantInline, TieredPricingRuleInline]
    search_fields = ('title',)
    list_filter = ('is_active',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'is_wholesale_order', 'created_at')
    list_filter = ('status', 'is_wholesale_order', 'created_at')
    search_fields = ('user__username', 'user__email')
    inlines = [OrderItemInline]
