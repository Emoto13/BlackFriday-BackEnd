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


from orders.views import OrdersViewSet
from products.views import ProductImagesViewSet, ProductsViewSet
from users.views import CustomUsersViewSet

from BlackFriday import settings
from orders.urls import order_urls
from products.urls import products_urls, cart_urls
from users.urls import user_urls

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

    path('user/', include(user_urls)),
    path('products/', include(products_urls)),
    path('order/', include(order_urls)),
    path('cart/', include(cart_urls)),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls

