from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from users.models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    country = CountryField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'description', 'city', 'street_and_number', 'floor', 'apartment',
                  'zip',
                  'is_staff', 'is_superuser', 'is_active', 'is_logged_in',
                  'last_login', 'date_joined', 'birthday', 'profile_image',
                  'account_title', 'latitude', 'longitude',
                  'gender', 'country']


class OrderCustomUserSerializer(serializers.HyperlinkedModelSerializer):
    country = CountryField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'country', 'city', 'street_and_number', 'floor', 'apartment',
                  'zip']
