# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product, ProductImage
from products.serializers import ProductSerializer, TestProductImageSerializer, ComplexProductSerializer
from django.db.models import F


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductImagesViewSet(viewsets.ModelViewSet):
    serializer_class = TestProductImageSerializer
    queryset = ProductImage.objects.all()


@api_view(['GET'])
def get_product(request, name):
    try:
        product = Product.objects.get(name=name)
        complex_product = ComplexProductSerializer(instance=product, context={"request": request})
        return Response(complex_product.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_product(request):
    product_data = request.data['product_data']
    product_images = request.data['product_images']

    if 'current_price' not in product_data.keys():
        product_data['current_price'] = product_data['original_price']

    product = Product.objects.create(**product_data)
    for image in product_images:
        ProductImage.objects.create(image=image, product=product)
    return Response('Product created successfully', status=status.HTTP_201_CREATED)


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
def get_discounted_products_by_category(request, category):
    product_objects = Product.objects.filter(current_price__lt=F('original_price')).filter(category=category)
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
