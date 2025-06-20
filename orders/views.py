from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    
    # Если корзина пуста - редирект с сообщением
    if not cart:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        
        if form.is_valid():
            try:
                # Создаем заказ
                order = form.save(commit=False)
                
                # Добавляем дополнительную логику перед сохранением
                if request.user.is_authenticated:
                    order.user = request.user
                
                order.save()
                
                # Создаем OrderItems
                items_created = []
                for item in cart:
                    product = item['product']
                    quantity = item['quantity']
                    price = product.sell_price()  # Используем актуальную цену
                    
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=price,
                        quantity=quantity
                    )
                    items_created.append(order_item)
                
                # Очищаем корзину только после успешного создания заказа
                cart.clear()
                
                # Сохраняем ID заказа в сессии для платежной системы
                request.session['order_id'] = order.id
                
                # Сообщение об успехе
                messages.success(request, f'Заказ #{order.id} успешно оформлен!')
                
                # Редирект на оплату
                return redirect(reverse('payment:process'))
                
            except Exception as e:
                # Откатываем изменения при ошибке
                if 'order' in locals():
                    order.delete()
                for item in items_created:
                    item.delete()
                    
                messages.error(request, f'Произошла ошибка при создании заказа: {str(e)}')
                return redirect('cart:cart_detail')
        else:
            # Обработка невалидной формы
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # GET запрос - инициализация формы
        form = OrderCreateForm(request=request)
    
    return render(request, 'order/create.html', {
        'cart': cart,
        'form': form,
        'section': 'orders'
    })

@require_POST
def order_remove(request, order_id):
    """Удаление заказа (только для POST запросов)"""
    try:
        order = Order.objects.get(id=order_id)
        
        # Проверяем, что заказ принадлежит пользователю
        if request.user.is_authenticated and order.user == request.user:
            order.delete()
            messages.success(request, 'Заказ успешно отменен')
        else:
            messages.error(request, 'Вы не можете отменить этот заказ')
            
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден')
    
    return redirect('orders:order_list')