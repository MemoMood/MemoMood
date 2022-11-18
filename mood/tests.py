from django.test import TestCase
from django.contrib.auth.models import User
from mood.models import FactorDetail, MoodFactors, SleepTimeField, UserDiary, Diary
from django.urls import reverse
from mood.views import *


class MeMoodModelTest(TestCase):
    def setUp(self) -> None:
        self.time_test = "2022-11-14"
        self.mood_factor = MoodFactors(factor="happy")
        self.factor_detail = FactorDetail(name="Alpha", category="Positive", detail="Main", factor=self.mood_factor, favorite="True")
        self.diary = Diary(time=self.time_test, place="KU", weather="Sunny", text="Hello")
        self.sleep_time = SleepTimeField(user=User(username="Harry"), day="2022-11-14", hour="8")

    def test_mood_factors(self):
        self.assertEqual("happy", self.mood_factor.factor)
        self.assertEqual("happy", str(self.mood_factor))

    def test_factor_detail(self):
        self.assertEqual("Alpha", self.factor_detail.name)
        self.assertEqual("Alpha", str(self.factor_detail))
        self.assertEqual("Positive", self.factor_detail.category)
        self.assertEqual("Main", self.factor_detail.detail)
        self.assertEqual(MoodFactors, type(self.factor_detail.factor))
        self.assertEqual("True", self.factor_detail.favorite)

    def test_diary(self):
        with self.assertRaises(ValueError):
            self.diary.mood.add(self.factor_detail.pk)
        self.assertEqual("2022-11-14", self.diary.time)
        self.assertEqual("KU", self.diary.place)
        self.assertEqual("Sunny", self.diary.weather)
        self.assertEqual("Hello", self.diary.text)
        self.assertEqual("Diary at 2022-11-14", str(self.diary))

    def test_sleep_time_field(self):
        self.assertEqual(User, type(self.sleep_time.user))
        self.assertEqual("Harry", self.sleep_time.user.username)
        self.assertEqual("2022-11-14", self.sleep_time.day)
        self.assertEqual("8", self.sleep_time.hour)
        self.assertEqual("2022-11-14 sleep 8 hour", str(self.sleep_time))

    def test_user_diary(self):
        user_diary = UserDiary(user=User(username="Hermione"))
        with self.assertRaises(ValueError):
            user_diary.diary.add(diary=self.diary)
            user_diary.factor.add(factor=self.factor_detail)
            user_diary.sleep_time.add(sleeptime=self.sleep_time)
        self.assertEqual("User diary name: Hermione", str(user_diary))


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
        self.assertRedirects(response, '/mood/profile')
        response = self.client.post(reverse('mood'), follow=True)
        self.assertRedirects(response, '/mood/profile')

    def test_mood_load(self):
        response = self.client.get(reverse('mood'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/home.html')

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
        logged_in = self.client.login(username='test_user', password='12345')
        self.assertTrue(logged_in)
        response = self.client.get('/accounts/login/?next=/mood/record', follow=True)
        self.assertRedirects(response, '/mood/record')
        response = self.client.post('/accounts/login/?next=/mood/record', follow=True)
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