from django.shortcuts import render, redirect, \
    get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.http import JsonResponse


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))  # Возврат на предыдущую страницу
    
    return redirect('cart:cart_detail')  # Если форма невалидна

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Пересчитываем все цены
        cart.get_total_price()
        return JsonResponse({
            'is_minimum_amount_reached': cart.is_minimum_amount_reached(),
            'total_price': cart.get_total_price()
        })
    
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'is_minimum_amount_reached': cart.is_minimum_amount_reached()
    })