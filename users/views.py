from functools import partial

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import CustomUserSerializer

from django.contrib.auth import logout


class CustomUsersViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = []


@api_view(['POST'])
def create_user(request):
    CustomUser.objects.create_user(**request.data)
    return Response('User creation successful', status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_user(request, username):
    user = CustomUser.objects.get(username=username)
    if user is None:
        return Response("No user with that username", status=status.HTTP_200_OK)
    return Response(CustomUserSerializer(user).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    CustomUser.objects.create_user(**request.data)
    return Response('User creation successful', status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_user(request):
    pass


@api_view(['GET'])
def user_logout(request):
    logout(request)
    return Response('Logged out successfully', status=status.HTTP_200_OK)
