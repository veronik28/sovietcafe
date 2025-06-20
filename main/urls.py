from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'main'

urlpatterns = [
    path('', views.popular_list, name='popular_list'),
    path('menu/', views.product_list, name='product_list'),
    path('menu/<slug:slug>/', views.product_detail, name = 'product_detail'),
    path('menu/category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('delivery/', views.delivery, name='delivery'),
]

