# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product, ProductImage
from products.serializers import ProductSerializer, ProductImageSerializer, ComplexProductSerializer, \
    TestProductImageSerializer


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
    images = request.data['images']

    product = Product.objects.create(**product_data)

    for image in images:
        ProductImage.objects.create(image=image, product=product)
    return Response('Product created successfully', status=status.HTTP_201_CREATED)
