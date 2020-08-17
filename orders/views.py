from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import OrderSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


@api_view(['POST'])
def create_order(request):
    print(request.user, request.auth)
    return Response(status=status.HTTP_201_CREATED)
