from rest_framework import serializers

from products.models import Product, ProductImage


class TestProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['url', 'id', 'name', 'type',
                  'original_price', 'current_price', 'discount_percentage',
                  'description', 'upload_date', 'country', 'city', 'in_store', ]


class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'uploaded_on']


class ProductImageRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        return data

    def to_representation(self, obj):
        return ProductImageSerializer(obj).data


class ComplexProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['url', 'id', 'name', 'type',
                  'original_price', 'current_price', 'discount_percentage',
                  'description', 'upload_date', 'country', 'city', 'in_store', 'product_images']
