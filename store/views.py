from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, ProductVariant

def storefront(request):
    # Initialize role in session if not set
    if 'role' not in request.session:
        request.session['role'] = 'RETAIL'
        
    products = Product.objects.filter(is_active=True).prefetch_related('pricing_tiers')
    
    return render(request, 'store/storefront.html', {
        'products': products,
        'role': request.session.get('role')
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    role = request.session.get('role', 'RETAIL')
    
    # Get active tier if wholesale
    active_tier = None
    if role == 'WHOLESALE':
        active_tier = product.pricing_tiers.first()
        
    return render(request, 'store/product_detail.html', {
        'product': product,
        'role': role,
        'active_tier': active_tier
    })

def toggle_role(request):
    current_role = request.session.get('role', 'RETAIL')
    request.session['role'] = 'WHOLESALE' if current_role == 'RETAIL' else 'RETAIL'
    messages.success(request, f"Switched view to {request.session['role']} portal.")
    return redirect(request.META.get('HTTP_REFERER', 'storefront'))

def cart_view(request):
    role = request.session.get('role', 'RETAIL')
    cart = request.session.get('cart', {})
    
    cart_items = []
    total_value = 0
    total_quantity = 0
    
    WHOLESALE_MOV = 1500.00
    WHOLESALE_MOQ = 20
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            
            # Pricing Logic
            price = float(product.base_wholesale_price) if role == 'WHOLESALE' else float(product.base_retail_price)
            
            # Apply Tier Discount if Wholesale
            if role == 'WHOLESALE':
                tier = product.pricing_tiers.filter(min_quantity__lte=quantity).order_by('-min_quantity').first()
                if tier:
                    discount = price * (float(tier.discount_percentage) / 100.0)
                    price = price - discount
                    
            item_total = price * quantity
            total_value += item_total
            total_quantity += quantity
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'item_total': item_total
            })
        except Product.DoesNotExist:
            continue
            
    can_checkout = True
    moq_warning = ""
    
    if role == 'WHOLESALE' and cart_items:
        if total_value < WHOLESALE_MOV and total_quantity < WHOLESALE_MOQ:
            can_checkout = False
            moq_warning = f"Wholesale minimums not met. Need ${WHOLESALE_MOV} total OR {WHOLESALE_MOQ} items."
            
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_value': total_value,
        'total_quantity': total_quantity,
        'role': role,
        'can_checkout': can_checkout,
        'moq_warning': moq_warning
    })

def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        
        str_id = str(product_id)
        if str_id in cart:
            cart[str_id] += quantity
        else:
            cart[str_id] = quantity
            
        request.session['cart'] = cart
        messages.success(request, "Added to cart.")
        
    return redirect('cart_view')

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
        messages.info(request, "Cart cleared.")
    return redirect('cart_view')
