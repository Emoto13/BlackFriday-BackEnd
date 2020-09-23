# Create your views here.
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils import timezone
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from BlackFriday import settings
from users.models import CustomUser
from users.serializers import CustomUserSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class CustomUsersViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = []


@cache_page(CACHE_TTL)
@permission_classes([IsAuthenticated])
@api_view(['GET', ])
def authenticated_user_information(request):
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def create_user(request):
    CustomUser.objects.create_user(**request.data)
    return Response('User creation successful', status=status.HTTP_201_CREATED)


@cache_page(CACHE_TTL)
@permission_classes([IsAuthenticated])
@api_view(['GET', ])
def get_user(request, username):
    user = CustomUser.objects.get(username=username)
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


@parser_classes([FileUploadParser])
@permission_classes([IsAuthenticated])
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


@cache_page(CACHE_TTL)
@api_view(['GET', ])
def search_users(request, query):
    users = CustomUser.objects.filter(username__icontains=query)
    return Response(CustomUserSerializer(instance=users, many=True, context={"request": request}).data,
                    status=status.HTTP_200_OK)


@api_view(['GET', ])
def restore_password(request, sender_email, password, receiver_email):
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           <a href="http://www.realpython.com">Real Python</a> 
           has many great tutorials.
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    return Response('Email with instruction sent', status=status.HTTP_200_OK)
