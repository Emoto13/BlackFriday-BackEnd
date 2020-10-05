from django.urls import path

from products.views import get_products, get_products_by_category, create_product, get_discounted_products, get_product, \
    cart_ids

products_urls = [
    path('', get_products),
    path('category/<str:category>/', get_products_by_category),
    path('create/', create_product),
    path('discounted/', get_discounted_products),
    path('discounted/category/<str:category>/', get_discounted_products),
    path('<str:url_name>/', get_product),
]

cart_urls = [
    path('ids/<str:ids>/', cart_ids),
]
