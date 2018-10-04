from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from web_service import models


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def signup(request):
    user = models.User.objects.create_user(
        username=request.POST['phone'],
        full_name=request.POST['full_name'],
        phone=request.POST['phone'],
        password=request.POST['password']
    )
    Token.objects.create(user=user).save()
    return Response({
        'success': True,
        'token': Token.objects.get(user=user).key
    })


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def login(request):
    user_query = models.User.objects.filter(phone=request.GET.get('phone'))
    if user_query.count() != 1:
        return Response({
            'success': 'false',
            'message': 'شماره تلفن و یا رمز عبور اشتباه است.'
        })
    user = user_query[0]
    pass_ok = user.check_password((request.GET.get('password')))
    if not pass_ok:
        return Response({
            'success': False,
            'message': 'شماره تلفن و یا رمز عبور اشتباه است.'
        })
    return Response({
        'success': True,
        'token': Token.objects.get(user=user).key,
        'fullname': user.full_name
    })
