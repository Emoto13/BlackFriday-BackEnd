from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from users.models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    country = CountryField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password',
                  'is_staff', 'is_active', 'last_login', 'date_joined',
                  'birthday', 'account_title', 'latitude', 'longitude',
                  'gender', 'country']
