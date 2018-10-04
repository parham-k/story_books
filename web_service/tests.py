from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token

from web_service import models, views


class TestServerAPI(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        admin = models.User.objects.create_user(
            username='admin',
            password='pass1234',
            is_staff=True,
        )
        self.admin = admin
        Token.objects.create(user=admin).save()

    def test_signup_and_login(self):
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
        request = self.factory.get(url, data=data)
        force_authenticate(request, self.admin, token=Token.objects.get(user=self.admin))
        response = views.login(request).data
        assert response['success'] and response['fullname'] == 'test user'
