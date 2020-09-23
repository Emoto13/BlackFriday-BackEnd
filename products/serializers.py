from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from products.models import Product, ProductImage
from drf_extra_fields.fields import Base64ImageField


class TestProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    country = CountryField()

    class Meta:
        model = Product
        fields = ['url', 'id', 'name', 'category',
                  'original_price', 'current_price', 'discount_percentage',
                  'description', 'upload_date', 'country', 'city', 'in_store', 'url_name']


class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'uploaded_on']


class ProductImageRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        return data

    def to_representation(self, obj):
        return ProductImageSerializer(instance=obj).data


class ComplexProductSerializer(serializers.HyperlinkedModelSerializer):
    product_images = ProductImageRelatedField(many=True, read_only=True)
    country = CountryField()

    class Meta:
        model = Product
        fields = ['url', 'id', 'name', 'category',
                  'original_price', 'current_price', 'discount_percentage',
                  'description', 'upload_date', 'country', 'city', 'in_store', 'product_images', 'url_name']
        lookup_field = 'url_name'


class MiniProductSerializer(serializers.HyperlinkedModelSerializer):
    product_images = ProductImageRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'current_price',
                  'description', 'product_images', 'url_name']


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    product_images = ProductImageRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'discount_percentage', 'country', 'in_store', 'product_images', 'url_name']
