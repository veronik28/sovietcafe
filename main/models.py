from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=[self.slug])

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    description = models.TextField(blank=True)
    composition = models.TextField('Состав', blank=True, null=True)  # Полностью необязательное
    
    # Пищевая ценность
    energy = models.PositiveIntegerField('Энергия, ккал', blank=True, null=True)
    fats = models.DecimalField('Жиры, г', max_digits=5, decimal_places=1, blank=True, null=True)
    carbohydrates = models.DecimalField('Углеводы, г', max_digits=5, decimal_places=1, blank=True, null=True)
    proteins = models.DecimalField('Белки, г', max_digits=5, decimal_places=1, blank=True, null=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
        ]
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('main:product_detail', args=[self.slug])
    
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images',
                              on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m%d', blank=True)

    def __str__(self):
        return f'{self.product.name} - {self.image.name}'