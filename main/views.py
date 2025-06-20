from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category
from cart.forms import CartAddProductForm
import random

def popular_list(request):
    all_products = list(Product.objects.all())
    random_products = random.sample(all_products, min(8, len(all_products)))
    context = {
        'random_products': random_products
    }
    return render(request, 'main/index/index.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug = slug)
    cart_product_form = CartAddProductForm
    return render(request, 'main/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})

def contacts(request):
    return render(request, 'main/contacts.html')

def about(request):
    return render(request, 'main/about.html')

def product_list(request, category_slug=None):
    page = request.GET.get('page', 1)
    category = None
    categories = Category.objects.all()
    # products = Product.objects.filter(available = True)
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    current_page = paginator.page(int(page))
    
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        paginator = Paginator(products.filter(category=category), 12)
        current_page = paginator.page(int(page))
        # products = products.filter(category=category)
    return render(request, 'main/product/list.html', {'category': category, 'categories': categories, 
                                                      'products': current_page, 'slug_url': category_slug})

def delivery(request):
    context = {
        'yandex_api_key': '98e0df28-87d3-429d-be61-9bd255fbcf59',
        'restaurant_address': 'ул. Красина, 27',
        'restaurant_coords': [55.760857, 37.606364],  # Координаты ул. Красина, 27
    }
    return render(request, 'main/delivery.html', context)