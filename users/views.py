from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import CustomUserSerializer

from django.contrib.auth import authenticate


class CustomUsersViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def auth_user(request):
    print(request.data, request.headers, request.user)
    #  user = authenticate(username=request.data['username'], password=request.data['password'])
    # request.user = user
    # print(user)
    print(request.user)
    return Response('Authenticated successfully', status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    user = CustomUser.objects.create_user(**request.data)
    return Response('User creation successful', status=status.HTTP_201_CREATED)
