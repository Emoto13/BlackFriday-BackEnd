# Create your views here.
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
import copy

from BlackFriday import settings
from products.models import Product, ProductImage
from products.serializers import ProductSerializer, TestProductImageSerializer, ComplexProductSerializer, \
    MiniProductSerializer, ProductImageSerializer
from django.db.models import F
from rest_framework.permissions import IsAuthenticated, IsAdminUser

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductImagesViewSet(viewsets.ModelViewSet):
    serializer_class = TestProductImageSerializer
    queryset = ProductImage.objects.all()


# Refactor to pe able to use id, name and url_name
@cache_page(CACHE_TTL)
@api_view(['GET', ])
def get_product(request, url_name):
    try:
        product_object = Product.objects.get(url_name=url_name)
        product = ComplexProductSerializer(instance=product_object, context={"request": request})
        return Response(product.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@parser_classes([FileUploadParser])
@permission_classes([IsAdminUser])
@api_view(['POST', ])
def create_product(request):
    product_images = request.data['images']
    product_data = dict(copy.deepcopy(request.data))
    product_data.pop('images', None)
    for key in request.data.keys():
        value = request.data[key]
        if 'images' != key:
            product_data[key] = value
#
    if 'current_price' not in product_data.keys():
        product_data['current_price'] = product_data['original_price']

    product = Product.objects.create(**product_data)

    for image in request.FILES.getlist('images'):
        ProductImage.objects.create(image=image, product=product)
    return Response('Product created successfully', status=status.HTTP_201_CREATED)


@cache_page(CACHE_TTL)
@permission_classes([IsAuthenticated])
@api_view(['GET', ])
def get_discounted_products(request, category=''):
    if category != '':
        product_objects = Product.objects.filter(current_price__lt=F('original_price')).filter(category=category)
        products = ComplexProductSerializer(instance=product_objects, many=True, context={'request': request})
        return Response(products.data, status=status.HTTP_200_OK)

    product_objects = Product.objects.filter(current_price__lt=F('original_price'))
    products = ComplexProductSerializer(instance=product_objects, many=True, context={'request': request})
    return Response(products.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def get_products_by_category(request, category=''):
    if category != '':
        product_objects = Product.objects.filter(category=category)
        products = ComplexProductSerializer(instance=product_objects, many=True, context={'request': request})
        return Response(data=products.data, status=status.HTTP_200_OK)

    product_objects = Product.objects.all()
    products = ComplexProductSerializer(instance=product_objects, many=True, context={'request': request})
    return Response(data=products.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def get_products(request):
    product_objects = Product.objects.all()
    products = ComplexProductSerializer(instance=product_objects, many=True, context={'request': request})
    return Response(products.data, status=status.HTTP_200_OK)


@cache_page(CACHE_TTL)
@api_view(['GET', ])
def cart_ids(request, ids):
    product_ids = ids.split("-")
    int_ids = list(map(lambda id: int(id), product_ids))
    product_objects = [Product.objects.get(id=int_id) for int_id in int_ids]
    products = MiniProductSerializer(instance=product_objects, many=True, context={"request": request})
    return Response(products.data, status=status.HTTP_200_OK)


@cache_page(CACHE_TTL)
@api_view(['GET', ])
def search_products(request, query):
    products = Product.objects.filter(name__icontains=query)
    return Response(MiniProductSerializer(instance=products, many=True, context={"request": request}).data,
                    status=status.HTTP_200_OK)
@cache_page(CACHE_TTL)
@api_view(['GET', ])
def recent_products(request, count):
    products = Product.objects.all()[:count]
    return Response(ComplexProductSerializer(instance=products, many=True, context={"request": request}).data,
                    status=status.HTTP_200_OK)
