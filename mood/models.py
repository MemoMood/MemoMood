import datetime
from django.db import models

# Create your models here.


class TodayMood(models.Model):
    date = models.DateTimeField(auto_now=True, blank=False, null=False)

    def no_mood(self):
        choice = ChoiceMood.objects.filter()
        return True

    def can_set(self):
        return True


class ChoiceMood(models.Model):
    mood = models.CharField(max_length=100, blank=False, null=False)
    mood_date = models.DateTimeField(auto_now=True, blank=False, null=False)
    today_mood = models.ForeignKey(TodayMood, blank=False, null=False, on_delete=models.CASCADE)


class Diary(models.Model):
    text = models.TextField(blank=False)
