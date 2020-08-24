from rest_framework import serializers

from orders.models import Order
from products.serializers import ProductSerializer
from users.serializers import CustomUserSerializer


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    ordered_by = CustomUserSerializer()
    ordered_product = ProductSerializer()

    class Meta:
        model = Order
        fields = ['id', 'ordered_by', 'ordered_product',
                  'order_date', 'delivery_date', 'delivery_price',
                  'status', 'total_price']
