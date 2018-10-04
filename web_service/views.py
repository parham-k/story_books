from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from web_service import models


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def signup(request):
    user = models.User(
        full_name=request.POST['full_name'],
        phone=request.POST['phone'],
        password=request.POST['password']
    )
    user.save()
    Token.objects.create(user=user).save()
    return Response({
        'success': True,
        'token': Token.objects.get(user=user).key
    })
