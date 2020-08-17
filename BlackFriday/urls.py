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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from BlackFriday import settings
from orders.views import OrdersViewSet, create_order
from users.views import CustomUsersViewSet, auth_user, create_user

router = routers.DefaultRouter()
router.register('users', CustomUsersViewSet)
router.register('orders', OrdersViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('create-order/', create_order),
    path('create-user/', create_user),
    path('auth_user/', auth_user)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


