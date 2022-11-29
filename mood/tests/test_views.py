from django.test import TestCase
from django.contrib.auth.models import User
from mood.models import *
from django.urls import reverse
from mood.views import *

class MeMoodViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.user.set_password('12345')
        self.user.save()

    def test_check_null(self):
        check = check_null()
        self.assertEqual(check, None)

    def test_welcome_load(self):
        self.client.login(username='test_user', password='12345')
        response = self.client.get(reverse('welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mood/welcome.html')
