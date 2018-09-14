from django.http import HttpResponse, Http404

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
