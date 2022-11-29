from django.test import TestCase
from django.contrib.auth.models import User
from mood.models import MoodFactors
from django.urls import reverse
from mood.views import MoodFactors, check_null


class MeMoodViewsAnonymousTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.user.set_password('12345')
        self.user.save()

    def test_check_null(self):
        self.assertQuerysetEqual([], MoodFactors.objects.all())
        check_null()
        with self.assertRaises(AssertionError):
            self.assertQuerysetEqual([], MoodFactors.objects.all())

    def test_welcome_load(self):
        response = self.client.get(reverse('welcome'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_mood_deny_anonymous(self):
        response = self.client.get(reverse('mood'), follow=True)
        self.assertRedirects(response, '/accounts/login/')
        response = self.client.post(reverse('mood'), follow=True)
        self.assertRedirects(response, '/accounts/login/')

    def test_mood_load(self):
        response = self.client.get(reverse('mood'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/base.html')

    def test_set_sleep_time_deny_anonymous(self):
        response = self.client.get('/mood/sleep_time', follow=True)
        self.assertRedirects(response, '/accounts/login/')
        response = self.client.post('/mood/sleep_time', follow=True)
        self.assertRedirects(response, '/accounts/login/')

    def test_set_sleep_time_load(self):
        response = self.client.get('/mood/sleep_time', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/base.html')

    def test_record_deny_anonymous(self):
        response = self.client.get('/mood/record', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/mood/record')
        response = self.client.post('/mood/record', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/mood/record')

    def test_record_load(self):
        response = self.client.get('/mood/record', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_profile_load(self):
        response = self.client.get('/mood/profile', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/home.html')
        self.assertTemplateUsed(response, 'account/base.html')

    def test_record_can_login(self):
        logged_in = self.client.login(username='test_user', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get('/accounts/login/?next=/mood/record',
                                   follow=True)
        self.assertRedirects(response, '/mood/record')
        response = self.client.post('/accounts/login/?next=/mood/record',
                                    follow=True)
        self.assertRedirects(response, '/mood/record')
        self.assertTemplateUsed(response, 'mood/record.html')


class MeMoodViewsUserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user')
        self.user.set_password('12345')
        self.user.save()
        self.client.login(username='test_user', password='12345')

    def test_welcome_load(self):
        response = self.client.get(reverse('welcome'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_mood_load(self):
        response = self.client.get(reverse('mood'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'dashboard/home.html')

    def test_set_sleep_time_load(self):
        response = self.client.get('/mood/sleep_time', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'dashboard/home.html')

    def test_record_load(self):
        response = self.client.get('/mood/record', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'account/login.html')

    def test_profile_load(self):
        response = self.client.get('/mood/profile', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/home.html')
        self.assertTemplateUsed(response, 'account/base.html')

    def test_add_place(self):
        response = self.client.get('/mood/add_place')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/mood/add_place')
        self.assertEqual(response.status_code, 200)

    def test_add_people(self):
        response = self.client.get('/mood/add_people')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/mood/add_people')
        self.assertEqual(response.status_code, 200)

    def test_discover(self):
        response = self.client.get('/mood/discover')
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/mood/discover')
        self.assertEqual(response.status_code, 302)

    def test_daily_mood(self):
        response = self.client.get('/mood/dailymood')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/mood/dailymood')
        self.assertEqual(response.status_code, 200)

    def test_accept_sleep_time(self):
        response = self.client.get('/mood/accept/sleep_time')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/mood/accept/sleep_time')
        self.assertEqual(response.status_code, 200)

    def test_accept_adding(self):
        response = self.client.get('/mood/accept/adding')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/mood/accept/adding')
        self.assertEqual(response.status_code, 200)
