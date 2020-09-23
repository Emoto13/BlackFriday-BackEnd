from rest_framework import serializers

from orders.models import Order
from products.serializers import OrderProductSerializer
from users.serializers import OrderCustomUserSerializer


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    ordered_by = OrderCustomUserSerializer()
    ordered_products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'ordered_by', 'ordered_products',
                  'order_date', 'delivery_date', 'delivery_price',
                  'status', 'total_price']

