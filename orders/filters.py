import django_filters
from django_filters import rest_framework as filters

from orders.models import Order


class OrderFilter(filters.FilterSet):

    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    release_year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
    release_year__gt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__gt')
    release_year__lt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__lt')

    manufacturer__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ['order_date', 'delivery_date', 'status', 'total_price']
