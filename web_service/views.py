import random
import requests
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from story_books_server.settings import PAYMENT_API_KEY
from web_service import models


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
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
        password=request.POST['password'],
    )
    user.sms_token = random.randint(10 ** 4, 10 ** 5)
    user.is_active = False
    user.save()
    # TODO: Send activation SMS
    Token.objects.create(user=user).save()
    return Response({
        'success': True,
        'token': Token.objects.get(user=user).key,
        'message': 'ثبت‌نام با موفقیت انجام شد.',
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def activate_profile(request):
    token = request.data['sms_token']
    if request.user.sms_token == token:
        request.user.is_active = True
        request.user.sms_token = None
        return Response({'success': True, 'message': 'کد فعالسازی تایید شد.'})
    return Response({'success': False, 'message': 'کد فعالسازی نادرست می‌باشد.'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def password_recovery(request):
    phone = request.data['phone']
    try:
        user = models.User.objects.get(phone=phone)
    except models.User.DoesNotExist:
        return Response({'success': False, 'message': 'کاربری بااین شماره پیدا نشد.'})
    # TODO Send recovery SMS
    return Response({'success': True, 'message': 'پیامک فراموشی به شماره شما ارسال شد.'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def set_recovered_password(request):
    phone = request.data['phone']
    code = request.data['code']
    password = request.data['password']
    try:
        user = models.User.objects.get(phone=phone)
    except models.User.DoesNotExist:
        return Response({'success': False, 'message': 'کاربری بااین شماره پیدا نشد.'})
    if code != user.sms_token:
        return Response({'success': False, 'message': 'کد وارد شده نادرست است.'})
    user.set_password(password)
    user.sms_token = None
    user.save()
    return Response({'success': True, 'message': 'رمز با موفقیت تغییر یافت.'})


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
        'books': owned_books,
        'message': '',
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def edit_profile(request):
    request.user.full_name = request.data['full_name']
    request.user.set_password(request.data['password'])
    request.user.save()
    return Response({'success': True, 'message': 'اطلاعات کاربری شما به روز شد.'})


@api_view(['GET'])
def shop(request):
    page = int(request.GET.get('page', 0))
    offset = int(request.GET.get('offset', 20))
    search = request.GET.get('filter')
    category = request.GET.get('category')
    books = list()
    start_index = page * offset
    end_index = min((page + 1) * offset, models.Book.objects.count())
    books_query = models.Book.objects.all()
    if search:
        books_query = books_query.filter(title__contains=search)
    if category:
        books_query = books_query.filter(categories__contains=[category])
    for book in books_query[start_index: end_index]:
        books.append({'id': book.pk, 'name': book.title, 'category': book.categories, 'image': book.cover.url})
    response_data = {'success': True, 'books': books}
    if page == 0:
        all_categories = set()
        for book in models.Book.objects.all():
            for category in book.categories:
                all_categories.add(category)
        response_data.update({'categories': list(all_categories)})
        slides = [{'is_book': True, 'image': slide.image.url, 'book_id': slide.book.pk} for slide in
                  models.Slide.objects.all() if slide.book is not None]
        slides += [{'is_book': False, 'image': slide.image.url, 'url': slide.url} for slide in
                   models.Slide.objects.all() if slide.book is None]
        response_data.update({'slides': slides})
    return Response(response_data)


@api_view(['GET'])
def book_info(request):
    pk = request.GET.get('id')
    if pk and models.Book.objects.filter(pk=pk).count() == 1:
        book = models.Book.objects.get(pk=pk)
        comments = []
        for comment in book.comments.filter(approved=True):
            comments.append({
                'user': comment.user,
                'text': comment.text,
                'date': comment.date,
            })
        return Response({
            'success': True,
            'id': book.pk,
            'name': book.title,
            'category': book.categories,
            'image': book.cover.url,
            'pages': book.pages.count(),
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


@api_view(['POST'])
def payment_request(request):
    user = request.user
    book = models.Book.objects.get(pk=int(request.data['book_id']))
    if book.price == 0:
        request.user.books.add(book)
        return Response({'success': True, 'message': 'کتاب با موفقیت خریداری شد.'})
    factor_number = '{}-{}'.format(user.pk, book.pk)
    data = {
        'api': PAYMENT_API_KEY,
        'amount': book.price * 10,
        'redirect': '',  # todo: callback url
        'mobile': request.user.phone,
        'factorNumber': factor_number,
        'description': 'خرید کتاب {}'.format(book.title),
    }
    payment = models.Payment(user=user, book=book, factor_number=factor_number)
    try:
        response = requests.post('https://pay.ir/payment/send', data).json()
        if response['status'] == 1:
            payment.transaction_id1 = response['transId']
            payment.factor_number = factor_number
            payment.save()
            return Response({
                'success': True,
                'message': 'درخواست پرداخت با موفقیت ارسال شد. لطفا در صفحه درگاه، پرداخت را تکمیل کنید.',
                'transaction_id': response['transId'],
                'factor_number': factor_number,
                'redirect_url': 'https://pay.ir/payment/gateway/{}'.format(response['transId']),
            })
        else:
            return Response({'success': False,
                             'message': 'خطای {}: {}'.format(response['errorCode'], response['errorMessage'])})
    except requests.exceptions.RequestException as err:
        return Response({'success': False, 'message': 'خطا در اتصال به درگاه پرداخت.'})


@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        status = request.POST['status']
        if status == 0:
            return render(request, 'payment_done.html', {'error': True, 'message': request.POST['message']})
        transaction_number = request.POST['transId']
        factor_number = request.POST['factorNumber']
        card_number = request.POST['cardNumber']
        trace_number = request.POST['traceNumber']
        payment = models.Payment.objects.get(pk=factor_number)
        payment.transaction_id2 = transaction_number
        payment.card_number = card_number
        payment.trace_number = trace_number
        payment.save()
        try:
            verify_data = {'api': PAYMENT_API_KEY, 'transId': int(payment.transaction_id1)}
            verify_request = requests.post('https://pay.ir/payment/verify', verify_data)
            response = verify_request.json()
            if response['status'] == 1:
                payment.payment_amount = response['amount']
                payment.payment_verified = True
                payment.save()
                return redirect(reverse('dashboard'))
            else:
                return render(request, 'payment_done.html', {'error': True, 'message': response['errorMessage']})
        except requests.exceptions.RequestException as err:
            return render(request, 'payment_done.html', {'error': True, 'message': str(err)})
    else:
        return redirect(reverse('dashboard'))


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_book(request):
    book_id = request.data['book_id']
    try:
        book = models.Book.objects.get(pk=int(book_id))
    except models.Book.DoesNotExist:
        return Response({'success': False, 'message': 'کتاب مورد نظر یافت نشد.'})
    if book not in request.user.books:
        return Response({'success': False, 'message': 'شما این کتاب را خریداری نکرده‌اید.'})
    pages = []
    for page in book.pages.all():
        pages.append({
            'id': page.pk,
            'image': page.image.url,
            'audio': page.audio.url,
            'text': page.text,
        })
    return Response({'success': True, 'book': pages})
