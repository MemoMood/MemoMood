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

    def test_mood_index(self):
        response = self.client.get('/mood')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account_login'))
        self.client.get(reverse('account_login'))
        self.client.login(username='test_user', password='12345')
        response = self.client.post('/mood')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mood/index.html')

    def test_old_mood(self):
        response = self.client.get('/mood/archive')
        self.client.get(reverse('account_login'))
        self.client.login(username='test_user', password='12345')
        self.assertEqual(response.status_code, 302)

    def test_set_sleep_time(self):
        response = self.client.get('/mood/sleep_time')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account_login'))
        self.client.get(reverse('account_login'))
        self.client.login(username='test_user', password='12345')
        response = self.client.get('/mood/accept/sleep_time')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'mood/accept_components/back_from_sleep_time.html')

    def test_record_page(self):
        response = self.client.get('/mood/record')
        self.assertEqual(response.status_code, 302)
        self.client.get(reverse('account_login'))
        self.client.login(username='test_user', password='12345')
        response = self.client.get('/mood/record')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mood/record.html')
        response = self.client.post('/mood/record')
        self.assertEqual(response.status_code, 200)

    def test_daily_mood(self):
        response = self.client.get('/mood/dailymood')
        self.assertEqual(response.status_code, 302)
        self.client.get(reverse('account_login'))
        self.client.login(username='test_user', password='12345')
        response = self.client.get('/mood/dailymood')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mood/daily_mood.html')
        response = self.client.post('/mood/dailymood')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mood/daily_mood.html')

    def test_discover(self):
        response = self.client.get('/mood/discover')
        self.assertEqual(response.status_code, 302)
        self.client.get(reverse('account_login'))
        self.client.login(username='test_user', password='12345')
        response = self.client.get('/mood/discover')
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/mood/discover')
        self.assertEqual(response.status_code, 302)

    def test_remove_mood(self):
        response = self.client.get('/mood/remove/mood')
        self.assertEqual(response.status_code, 302)
        self.client.get(reverse('account_login'))
        self.client.login(username='test_user', password='12345')