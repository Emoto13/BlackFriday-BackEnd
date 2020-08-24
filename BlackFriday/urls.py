"""BlackFriday URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, register_converter
from rest_framework import routers

from BlackFriday import settings
from orders.views import OrdersViewSet, create_order, get_order_by_id, get_orders_by_status, \
    get_orders_by_delivery_date, get_orders_by_order_date
from products.views import ProductImagesViewSet, ProductsViewSet, get_product, create_product
from users.views import CustomUsersViewSet, user_logout, get_user, create_user, delete_user

router = routers.DefaultRouter()
router.register('users', CustomUsersViewSet)
router.register('orders', OrdersViewSet)
router.register('products', ProductsViewSet)
router.register('product-images', ProductImagesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

    path('users/<str:username>/', get_user),
    path('users-create/', create_user),
    #  path('users/update/<str:username>/', ),
    path('users-delete/<str:username>/', delete_user),
    path('logout/', user_logout),

    path('products/<str:name>', get_product),
    path('products-create/', create_product),

    path('get-order/<int:order_id>/', get_order_by_id),
    path('get-orders/status/<str:order_status>/', get_orders_by_status),
    path('get-orders/delivery-date/<str:delivery_date>/', get_orders_by_delivery_date),
    path('get-orders/order-date/<str:order_date>/', get_orders_by_order_date),
    path('create-order/', create_order),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls

