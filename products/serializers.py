from rest_framework import serializers
from products.models import Product, ProductImage


class TestProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
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

    class Meta:
        model = Product
        fields = ['url', 'id', 'name', 'category',
                  'original_price', 'current_price', 'discount_percentage',
                  'description', 'upload_date', 'country', 'city', 'in_store', 'product_images', 'url_name']

