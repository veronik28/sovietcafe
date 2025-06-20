from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('user-agreement/', views.user_agreement, name='user_agreement'),
    
]