from decimal import Decimal

from django.db import models

# Create your models here.
from django.utils import timezone
from django_countries.fields import CountryField
from drf_extra_fields.fields import Base64ImageField
from imagekit.forms import ProcessedImageField
from pilkit.processors import ResizeToFill

CATEGORIES = [
    ('A', 'Automotive'),
    ('B', 'Baby'),
    ('C', 'Computers'),
    ('F', 'Free'),
    ('S', 'Software'),
    ('BF', "Boys' Fashion"),
    ('GF', "Girl' Fashion"),
    ('MF', "Men's Fashion"),
    ('WF', "Women's Fashion"),
    ('HG', 'House and Garden'),
    ('RE', 'Real Estate'),
    ('SBH', 'Sports, Books, Hobby'),
    ('MTE', 'Machines, Tools, Equipment'),
]


# add ratings
class Product(models.Model):
    name = models.CharField(max_length=150, default='', unique=True)
    category = models.CharField(max_length=30, choices=CATEGORIES)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    description = models.TextField(default='')
    upload_date = models.DateTimeField(auto_now_add=True)
    country = CountryField(blank=True, blank_label='Select country', default='BG')
    city = models.CharField(max_length=150, default='')
    in_store = models.IntegerField(default=1)
    url_name = models.CharField(max_length=200, )

    def save(self, *args, **kwargs):
        self.discount_percentage = Decimal(100) - ((Decimal(self.current_price) / Decimal(self.original_price)) * Decimal(100))
        self.url_name = self.name.replace(' ', '-')
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.current_price} {self.in_store}'


class ProductImage(models.Model):
    image = models.ImageField(blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="product_images")
    uploaded_on = models.DateTimeField(auto_now_add=True)
    #image1 = ProcessedImageField(processors=[ResizeToFill(100, 50)],
    #                             spec_id='BlackFriday:product:image')
    #                             #default='/BlackFriday/static/media/defaults/')
