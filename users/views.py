from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, UserRegistrationForm, \
    ProfileForm
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from orders.models import Order, OrderItem
from django.utils import timezone


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,
                                     password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:product_list'))
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Не сохраняем сразу, чтобы добавить дополнительные поля
            user.agree_to_policy = form.cleaned_data.get('agree_to_policy', False)
            
            if user.agree_to_policy:
                user.policy_agreement_date = timezone.now()
            
            # Сохраняем телефон, если он был указан
            phone = form.cleaned_data.get('phone')
            if phone:
                user.phone = phone
            
            user.save()  # Теперь сохраняем пользователя со всеми данными
            
            auth.login(request, user)
            messages.success(request, f'{user.username}, Successful Registration')
            return HttpResponseRedirect(reverse('user:login'))
        else:
            # Если форма невалидна, покажем ошибки
            return render(request, 'users/registration.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user,
                           files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile was changed')
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)
    
    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            'items',
            queryset=OrderItem.objects.select_related('product'),
        )
    ).order_by('-id')
    return render(request, 'users/profile.html',
                  {'form': form,
                   'orders': orders})


def logout(request):
    auth.logout(request)
    return redirect(reverse('main:product_list'))

def privacy_policy(request):
    return render(request, 'users/privacy_policy.html')

def user_agreement(request):
    return render(request, 'users/user_agreement.html')