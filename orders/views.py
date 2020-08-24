# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import OrderSerializer
from orders.validators import date_handler
from products.models import Product


class OrdersViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


# get order by date, status, id
@api_view(['GET'])
def get_order_by_id(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        return Response(OrderSerializer(order, context={'request': request}).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_orders_by_status(request, order_status):
    orders = Order.objects.filter(status=order_status)
    return Response(OrderSerializer(orders, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@date_handler
def get_orders_by_delivery_date(request, year_month_date):
    try:
        orders = Order.objects.filter(delivery_date__year=year_month_date[0],
                                      delivery_date__month=year_month_date[1],
                                      delivery_date__day=year_month_date[2])
        return Response(OrderSerializer(orders, many=True, context={"request": request}).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response('No orders with that delivery date', status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@date_handler
def get_orders_by_order_date(request, year_month_date):
    try:
        orders = Order.objects.filter(order_date__year=year_month_date[0],
                                      order_date__month=year_month_date[1],
                                      order_date__day=year_month_date[2])
        return Response(OrderSerializer(orders, many=True, context={"request": request}).data,
                        status=status.HTTP_200_OK)
    except Exception as e:
        return Response('No orders with that order date', status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_order(request):
    user = request.user
    product = Product.objects.get(name=request.data['product_name'])
    order_data = {**{'ordered_by': user, 'ordered_product': product}, **request.data['order_data']}
    Order.objects.create(**order_data)
    return Response('Order has been successfully made', status=status.HTTP_201_CREATED)
