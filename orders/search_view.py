# filter fields => order_date, delivery_date, category, status, total_price, time(month, year), username, country, city
import json
from datetime import datetime

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from BlackFriday import settings
from orders.models import Order
from orders.serializers import OrderSerializer


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
@api_view(['GET', ])
def search_order(request, str_filters):
    filters = json.loads(str_filters)
    filter_orders = {
        'order_date': handle_order_date,
        'delivery_date': handle_delivery_date,
        'category': handle_category,
        'status': handle_status,
        'total_price': handle_total_price,
        'time_period': handle_time_period,
        'username': handle_username,
        'country': handle_country,
        'city': handle_city
    }
    orders = []
    for key in filters.keys():
        print(orders)
        filter_argument = filters[key]
        function = filter_orders[key]
        if not orders:
            orders = function(filter_argument)
        else:
            orders = function(filter_argument, orders=orders)
    orders = orders.distinct()
    serializer = OrderSerializer(instance=orders, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def handle_order_date(order_date, orders=Order.objects):
    return orders.filter(order_date=order_date)


def handle_delivery_date(delivery_date, orders=Order.objects):
    return orders.filter(delivery_date=delivery_date)


def handle_category(category, orders=Order.objects):
    return orders.filter(ordered_products__category=category)


def handle_status(order_status, orders=Order.objects):
    return orders.filter(status=order_status)


def handle_total_price(total_price, orders=Order.objects):
    return orders.filter(total_price=total_price)


# must include start and end
def handle_time_period(time_period, orders=Order.objects):
    start = datetime.strptime(time_period['start'], "%a, %d %b %Y %H:%M:%S %Z")
    end = datetime.strptime(time_period['end'], "%a, %d %b %Y %H:%M:%S %Z")
    orders_in_range = orders.filter(order_date__gte=start).filter(order_date__lte=end)
    return orders_in_range


def handle_username(username, orders=Order.objects):
    return orders.filter(ordered_by__username=username)


def handle_country(country, orders=Order.objects):
    return orders.filter(ordered_products__country=country)


def handle_city(city, orders=Order.objects):
    return orders.filter(ordered_prodcuts__city=city)
