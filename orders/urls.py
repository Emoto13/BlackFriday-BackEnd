from django.urls import path

from orders.search_view import search_order
from orders.views import get_order_by_id, create_order, recent_orders

order_urls = [
    path('<int:order_id>/', get_order_by_id),
    path('create/', create_order),
    path('search/<str:str_filters>', search_order),
    path('recent/', recent_orders)
]
