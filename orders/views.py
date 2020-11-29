# Create your views here.
from decimal import Decimal

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models.expressions import F
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from BlackFriday import settings
from orders.models import Order, OrderProduct
from orders.serializers import OrderSerializer
from products.models import Product

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class OrdersViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


# get order by date, status, id
@permission_classes([IsAdminUser])
@api_view(['GET', ])
def get_order_by_id(request, order_id):
    order = Order.objects.get(id=order_id)
    order_serializer = OrderSerializer(instance=order, context={'request': request})
    return Response(order_serializer.data, status=status.HTTP_200_OK)


# DEPRECATED
# @permission_classes([IsAuthenticated])
# @api_view(['POST'])
# def create_order(request):
#    print(request.user)
#    user = request.user
#    product = Product.objects.get(name=request.data['product_name'])
#    order_data = {**{'ordered_by': user, 'ordered_product': product}, **request.data['order_data']}
#    Order.objects.create(**order_data)
#    return Response('Order has been successfully made', status=status.HTTP_201_CREATED)

@cache_page(CACHE_TTL)
@permission_classes([IsAuthenticated])
@api_view(['POST', ])
def create_order(request):
    product_ids_and_quantity = request.data["product_ids_and_quantity"]
    order_data = {**request.data['order_data']}
    products = []
    total_price = Decimal(4.99)

    if 'delivery_price' in order_data:
        total_price = Decimal(order_data['delivery_price'])

    for product_id in product_ids_and_quantity.keys():
        quantity = product_ids_and_quantity[product_id]

        product = Product.objects.get(id=product_id)
        product.in_store = F('in_store') - quantity
        product.save()

        total_price += product.current_price * quantity

        for i in range(0, product_ids_and_quantity[product_id]):
            products.append(product)

    order_data = {'ordered_by': request.user, 'total_price': total_price, **request.data['order_data']}
    order = Order.objects.create(**order_data)

    for product in products:
        OrderProduct.objects.create(product=product, order=order,
                                    product_quantity=product_ids_and_quantity[str(product.id)])
    return Response('Order has been successfully made', status=status.HTTP_201_CREATED)


@permission_classes([IsAdminUser])
@api_view(['GET', ])
def recent_orders(request):
    orders = Order.objects.all()[:10]
    serializer = OrderSerializer(instance=orders, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
