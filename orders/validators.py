from django.core.exceptions import ValidationError
import re

def validate_phone(value):
    """Универсальный валидатор телефона, принимающий любые форматы"""
    if not value:
        raise ValidationError("Телефон не может быть пустым")
    
    # Удаляем все нецифровые символы кроме +
    phone = re.sub(r'[^\d+]', '', value)
    
    # Российские номера
    if phone.startswith('8') and len(phone) == 11:
        return  # Принимаем 89...
    elif phone.startswith('+7') and len(phone) == 12:
        return  # Принимаем +79...
    elif phone.startswith('7') and len(phone) == 11:
        return  # Принимаем 79...
    elif len(phone) == 10 and phone.startswith('9'):
        return  # Принимаем 9...
    
    # Международные номера (минимум 5 цифр)
    if phone.startswith('+') and len(re.sub(r'[^\d]', '', phone)) >= 5:
        return
    
    raise ValidationError("Введите корректный номер телефона. Российские номера должны начинаться с 8, +7 или 7 и содержать 11 цифр, или с 9 и содержать 10 цифр. Международные номера должны начинаться с + и содержать не менее 5 цифр.")