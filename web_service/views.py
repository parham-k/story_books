import json

from django.contrib.auth.models import Group, User
from django.http import HttpResponse, Http404
from rest_framework import viewsets

from web_service.models import *
from web_service.serializers import UserSerializer, GroupSerializer


def get_book(request, id):
    if Book.objects.filter(pk=id).count() == 1:
        response_data = Book.objects.get(pk=id).get_dict()
        return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type='application/json')
    else:
        raise Http404()


def get_latest_books(request):
    count = request.GET.get('count', '10')
    response_data = dict()
    latest_books = Book.objects.all()[:int(count)]
    for book in latest_books:
        response_data.update({book.pk: {
            'title': book.title,
            'text': book.text.url,
            'date_added': book.date_added.isoformat(),
        }})
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
