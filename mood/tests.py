from django.test import TestCase
from django.contrib.auth.models import User
from mood.models import FactorDetail, MoodFactors, SleepTimeField, UserDiary, Diary
from django.urls import reverse
from mood.views import *


class MeMoodModelTest(TestCase):

    def test_mood_factors(self):
        mood_factor = MoodFactors(factor="happy")
        self.assertEqual("happy", mood_factor.factor)
        self.assertEqual("happy", str(mood_factor))

    def test_factor_detail(self):
        factor_detail = FactorDetail(name="Alpha", category="Positive", detail="Main", favorite="True")
        self.assertEqual("Alpha", factor_detail.name)
        self.assertEqual("Alpha", str(factor_detail))
        self.assertEqual("Positive", factor_detail.category)
        self.assertEqual("Main", factor_detail.detail)
        self.assertEqual("True", factor_detail.favorite)

    def test_diary(self):
        diary = Diary(time="2022-11-14")
        self.assertEqual("2022-11-14", diary.time)
        self.assertEqual("Diary at 2022-11-14", str(diary))

    def test_sleep_time_field(self):
        sleep_time = SleepTimeField(day="2022-11-14", hour="8")
        self.assertEqual("2022-11-14 sleep 8 hour", str(sleep_time))

    def test_user_diary(self):
        user_diary = UserDiary(user=User(username="David"))
        self.assertEqual("User diary name: David", str(user_diary))


class MeMoodViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.user.set_password('12345')
        self.user.save()

    def test_mood_deny_anonymous(self):
        response = self.client.get(reverse('mood'), follow=True)
        self.assertRedirects(response, '/mood/profile')
        response = self.client.post(reverse('mood'), follow=True)
        self.assertRedirects(response, '/mood/profile')

    def test_mood_load(self):
        response = self.client.get(reverse('mood'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/home.html')

    def test_mood(self):
        pass

    def test_set_sleep_time_deny_anonymous(self):
        response = self.client.get('/mood/sleep_time', follow=True)
        self.assertRedirects(response, '/mood/profile')
        response = self.client.post('/mood/sleep_time', follow=True)
        self.assertRedirects(response, '/mood/profile')

    def test_set_sleep_time_load(self):
        response = self.client.get('/mood/sleep_time', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/home.html')

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
        logged_in = self.client.login(username='testuser', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get('/accounts/login/?next=/mood/record', follow=True)
        self.assertRedirects(response, '/mood/record')
        response = self.client.post('/accounts/login/?next=/mood/record', follow=True)
        self.assertRedirects(response, '/mood/record')
        self.assertTemplateUsed(response, 'mood/record.html')

    def test_add_place(self):
        pass

    def test_add_people(self):
        pass

    def test_add_mood_list(self):
        pass

    def test_discover(self):
        pass

    def test_accept_adding(self):
        pass