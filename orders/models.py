from datetime import timedelta
from functools import partial

from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.datetime_safe import datetime



def should_send_date(integer_days_to_add, current_date=timezone.now()):
    print(integer_days_to_add)
    raise Exception('Raised exception')
    return current_date


class Order(models.Model):
    # ordered_by = models.ForeignKey(CustomUser, related_name='ordered_by', on_delete=models.PROTECT, null=True)
    # ordered_product = models.ForeignKey(Product, related_name='ordered_product', on_delete=models.PROTECT, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_days = models.IntegerField(default=1)
    delivery_price = models.DecimalField(max_digits=4, decimal_places=2)
    day_of_sending = models.DateTimeField(default=partial(should_send_date, delivery_days))
