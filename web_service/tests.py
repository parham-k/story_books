from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token

from web_service import models, views


class TestServerAPI(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = models.User.objects.create_user(
            username='admin',
            password='pass1234',
            is_staff=True,
        )
        Token.objects.create(user=self.admin).save()
        self.client = models.User.objects.create_user(username='09133333333', password='pass1234')
        self.client.phone = '09133333333'
        self.client.full_name = 'test client'
        self.client.save()
        Token.objects.create(user=self.client).save()

        for i in range(100):
            models.Book(
                title=f'کتاب {i}',
                categories=[f'دسته{i}', f'دسته{i+1}', f'دسته{i+2}']
            ).save()
        for book in models.Book.objects.all()[:10]:
            self.client.books.add(book)
            slide = models.Slide(book=book, image='upload/books/1/image')
            slide.save()
            book.slides.add(slide)

    def test_signup(self):
        url = reverse('signup')
        data = {
            "full_name": "test user",
            "phone": "09131112233",
            "password": "user1234",
        }
        request = self.factory.post(url, data=data)
        force_authenticate(request, self.admin, token=Token.objects.get(user=self.admin))
        response = views.signup(request).data
        assert response['success'] and models.User.objects.filter(phone='09131112233').count() == 1

        url = reverse('login')
        data = {"phone": "09131112233", "password": "user1234"}
        request = self.factory.post(url, data=data)
        force_authenticate(request, self.admin, token=Token.objects.get(user=self.admin))
        response = views.login(request).data
        assert response['success'] and response['full_name'] == 'test user'

    def test_login(self):
        url = reverse('login')
        data = {'phone': '09133333333', 'password': 'pass1234'}
        request = self.factory.post(url, data=data)
        force_authenticate(request, self.admin, token=Token.objects.get(user=self.admin))
        response = views.login(request).data
        assert response['success'] and response['full_name'] == 'test client' and len(response['books']) == 10

    def test_shop(self):
        url = reverse('shop')
        data = {"page": "0", "categories": ["دسته3", "دسته5"], "filter": "کتاب 4"}
        request = self.factory.get(url, data=data)
        force_authenticate(request, self.admin, token=Token.objects.get(user=self.client))
        response = views.shop(request).data
        assert response['success'] and 'کتاب 4' in [book['name'] for book in response['books']]

    def test_book_info(self):
        url = reverse('book_info')
        data = {'id': models.Book.objects.all()[0].pk}
        request = self.factory.get(url, data=data)
        force_authenticate(request, self.admin, token=Token.objects.get(user=self.client))
        response = views.book_info(request).data
        assert response['success'] and response['name'] == models.Book.objects.all()[0].title

    def test_purchase(self):
        url = reverse('purchase')
        data = {'id': [b.pk for b in models.Book.objects.all()[10:15]]}
        request = self.factory.post(url, data=data)
        force_authenticate(request, self.admin, token=Token.objects.get(user=self.client))
        response = views.purchase(request).data
        assert response['success'] and response['message'].startswith('5')
