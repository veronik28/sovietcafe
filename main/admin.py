from django.contrib import admin

from .models import Product, Category, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug' : ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'discount']
    list_editable = ['price', 'discount']
    prepopulated_fields = {'slug' : ('name',)}
    inlines = [ProductImageInline]