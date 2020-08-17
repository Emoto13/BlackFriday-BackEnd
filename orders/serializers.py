from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'order_date', 'delivery_days', 'delivery_price', 'day_of_sending']
