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
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from BlackFriday import settings
from orders.search_view import search_order
from orders.views import OrdersViewSet, create_order, get_order_by_id
from products.views import ProductImagesViewSet, ProductsViewSet, get_product, create_product, get_discounted_products, \
    get_products_by_category, get_products, cart_ids
from users.views import CustomUsersViewSet, get_user, create_user, update_user, delete_user, \
    authenticated_user_information, search_users, restore_password

router = routers.DefaultRouter(trailing_slash=False)
router.register('users', CustomUsersViewSet)
router.register('orders', OrdersViewSet)
router.register('products', ProductsViewSet)
router.register('product-images', ProductImagesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('user/', authenticated_user_information),
    path('user/create/', create_user),
    path('user/update/', update_user),
    path('user/delete/', delete_user),
    path('user/<str:username>/', get_user),
    path('user/search/<str:query>/', search_users),
    path('restore-password/', restore_password),

    path('products/', get_products),
    path('products/category/<str:category>/', get_products_by_category),
    path('products/create/', create_product),
    path('products/discounted/', get_discounted_products),
    path('products/discounted/category/<str:category>/', get_discounted_products),
    path('products/<str:url_name>/', get_product),
    path('cart/ids/<str:ids>/', cart_ids),

    path('order/<int:order_id>/', get_order_by_id),
    path('order/create/', create_order),
    # path('order/create/test/', create_order_new),
    path('order/search/<str:str_filters>', search_order)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls

