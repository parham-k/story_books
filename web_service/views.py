import json

from django.http import HttpResponse, Http404, JsonResponse

from web_service.models import *


def get_book(request, title):
    if Book.objects.filter(title=title).count() == 1:
        book = Book.objects.get(title=title)
        zip_file = open(book.get_zip_filename(), 'rb')
        response = HttpResponse(zip_file, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(book.title)
        return response
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
