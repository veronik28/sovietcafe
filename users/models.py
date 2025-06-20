from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', blank=True, null=True)
    phone = models.CharField(max_length=18, blank=True, null=True, verbose_name="Телефон")
    
    # Добавляем новые поля для согласия с политикой
    agree_to_policy = models.BooleanField(
        'Согласие с политикой конфиденциальности',
        default=False
    )
    policy_agreement_date = models.DateTimeField(
        'Дата согласия с политикой',
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'user'
    
    def __str__(self):
        return self.username