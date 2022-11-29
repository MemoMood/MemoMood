from django.test import TestCase
from django.contrib.auth.models import User
from mood.models import FactorDetail, MoodFactors, SleepTimeField, UserDiary, Diary
from mood.views import MoodFactors, FactorDetail, Diary, SleepTimeField, UserDiary


class MeMoodModelTest(TestCase):
    def setUp(self) -> None:
        self.time_test = "2022-11-14"
        self.mood_factor = MoodFactors(factor="happy")
        self.factor_detail = FactorDetail(name="Alpha",
                                          category="Positive", detail="Main",
                                          factor=self.mood_factor,
                                          favorite="True")
        self.diary = Diary(time=self.time_test,
                           place="KU", weather="Sunny", text="Hello")
        self.sleep_time = SleepTimeField(user=User(username="Harry"),
                                         day="2022-11-14", hour="8")

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
