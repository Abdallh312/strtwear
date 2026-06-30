from django.urls import path
from . import views

urlpatterns = [
    path('', views.storefront, name='storefront'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('toggle-role/', views.toggle_role, name='toggle_role'),
]
