from django.db import models

# Create your models here.
from django.utils import timezone
from django_countries.fields import CountryField


class Product(models.Model):
    name = models.CharField(max_length=150)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField(default='')
    upload_date = models.DateTimeField(default=timezone.now)
    country = CountryField(blank=True, blank_label='Select country')
    city = models.CharField(max_length=150, default='')
    in_store = models.IntegerField()
    # product catalog


class ProductImage(models.Model):
    image = models.ImageField(blank=True)


class ProductImageCatalog(models.Model):
    product = models.ForeignKey(Product, related_name="product", on_delete=models.PROTECT)
    product_image = models.ForeignKey(ProductImage, related_name="product_image", on_delete=models.PROTECT)
    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "product_image")
        ordering = ["created"]

    def __str__(self):
        return f"{self.product} has {self.product_image}"
