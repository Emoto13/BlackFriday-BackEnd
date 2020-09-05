# Create your views here.
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from users.models import CustomUser
from users.permissions import AllowOptionsAuthentication
from users.serializers import CustomUserSerializer


class CustomUsersViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = []


@permission_classes([IsAuthenticated])
@api_view(['GET', ])
def authenticated_user_information(request):
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def create_user(request):
    CustomUser.objects.create_user(**request.data)
    return Response('User creation successful', status=status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
@api_view(['GET', ])
def get_user(request, username):
    user = CustomUser.objects.get(username=username)
    if user is None:
        return Response("No user with that username", status=status.HTTP_200_OK)
    return Response(CustomUserSerializer(user).data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def create_user(request):
    CustomUser.objects.create_user(**request.data)
    return Response('User creation successful', status=status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
@api_view(['DELETE', ])
def delete_user(request):
    if request.method == "DELETE":
        request.user.delete()
        return Response(data='Deletion successful')
    return Response(data='Deletion failed')


@api_view(['PATCH', ])
def update_user(request):
    data = request.data
    if 'is_logged_in' in request.data.keys():
        data['last_login'] = timezone.now()
    serializer = CustomUserSerializer(instance=request.user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response('Successfully updated', status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
