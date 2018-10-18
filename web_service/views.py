from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from web_service import models


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def signup(request):
    if models.User.objects.filter(phone=request.POST['phone']).count() == 1:
        return Response({
            'success': False,
            'message': 'کاربری با این شماره تلفن قبلاً ثبت‌نام کرده.',
        })
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


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def login(request):
    user_query = models.User.objects.filter(phone=request.POST['phone'])
    if user_query.count() != 1:
        return Response({
            'success': False,
            'message': 'شماره تلفن و یا رمز عبور اشتباه است.'
        })
    user = user_query[0]
    pass_ok = user.check_password((request.POST['password']))
    if not pass_ok:
        return Response({
            'success': False,
            'message': 'شماره تلفن و یا رمز عبور اشتباه است.'
        })
    owned_books = list()
    for book in user.books.all():
        owned_books.append({
            'id': book.pk,
            'name': book.title,
            'categories': book.categories,
            'image': book.cover.url,
        })
    return Response({
        'success': True,
        'token': Token.objects.get(user=user).key,
        'full_name': user.full_name,
        'books': owned_books
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def shop(request):
    page = int(request.GET.get('page', 0))
    offset = int(request.GET.get('offset', 20))
    search = request.GET.get('filter')
    categories = request.GET.getlist('categories')
    books = list()
    start_index = page * offset
    end_index = min((page + 1) * offset, models.Book.objects.count())
    books_query = models.Book.objects.all()
    if search:
        books_query = books_query.filter(title__contains=search)
    if categories:
        books_query = books_query.filter(categories__overlap=categories)
    for book in books_query[start_index: end_index]:
        books.append({'id': book.pk, 'name': book.title, 'category': book.categories})
    response_data = {'success': True, 'books': books}
    if page == 0:
        all_categories = set()
        for book in models.Book.objects.all():
            for category in book.categories:
                all_categories.add(category)
        response_data.update({'categories': list(all_categories)})
        slides = [{'id': slide.book.pk, 'image': slide.image.url} for slide in models.Slide.objects.all()]
        response_data.update({'slides': slides})
    return Response(response_data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def book_info(request):
    pk = request.GET.get('id')
    if pk and models.Book.objects.filter(pk=pk).count() == 1:
        book = models.Book.objects.get(pk=pk)
        pages = []
        for page in book.pages.all():
            pages.append({
                'number': page.number,
                'image': page.image.url,
                'audio': page.audio.url,
                'text': page.text,
            })
        comments = []
        for comment in book.comments.filter(approved=True):
            comments.append({
                'user': comment.user,
                'text': comment.text,
                'date': comment.date,
            })
        return Response({
            'success': True,
            'token': Token.objects.get(user=request.user).key,
            'id': book.pk,
            'name': book.title,
            'category': book.categories,
            'image': book.cover.url,
            'pages': pages,
            'ages': book.ages,
            'story': book.summary,
            'writer': book.author,
            'size': book.pages.count(),
            'price': book.price,
            'comments': comments
        })


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def purchase(request):
    if models.User.objects.filter(phone=request.POST['phone']).count() != 1:
        return Response({'success': False, 'message': 'کاربر یافت نشد.'})
    user = models.User.objects.get(phone=request.POST['phone'])
    book_ids = request.POST.getlist('id')
    success_count = 0
    for book_id in book_ids:
        if models.Book.objects.filter(pk=book_id).count() == 1:
            book = models.Book.objects.get(pk=book_id)
            if book not in user.books.all():
                user.books.add(book)
                success_count += 1
    if success_count > 0:
        return Response({'success': True, 'message': f'{success_count} کتاب به کتاب‌های شما افزوده شدند.'})
    else:
        return Response({'success': False, 'message': 'کتابی به کتاب‌های شما افزوده نشد.'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_app_info(request):
    return Response(dict((o.key, o.value) for o in models.AppInfo.objects.all()))


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_comment(request):
    user = request.user
    book_id = int(request.POST['book'])
    if models.Book.objects.filter(pk=book_id).count() != 1:
        return Response({
            'success': False,
            'message': 'کتاب مورد نظر یافت نشد.'
        })
    book = models.Book.objects.get(pk=book_id)
    text = request.POST['text']
    comment = models.Comment(
        user=user,
        book=book,
        text=text,
    )
    comment.save()
    return Response({
        'success': True,
        'message': 'نظر شما ثبت شد و پس از تأیید، نمایش داده خواهد شد.'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_feedback(request):
    user = request.user
    text = request.POST['text']
    feedback = models.Feedback(user=user, text=text)
    feedback.save()
    return Response({
        'success': True,
        'message': 'پیام شما ثبت شد.'
    })
