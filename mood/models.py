from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MoodFactors(models.Model):
    factor = models.CharField(
        max_length=255, unique=True, null=False, blank=False)

    def __str__(self) -> str:
        return self.factor


class FactorDetail(models.Model):
    factor = models.ForeignKey(MoodFactors, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    category = models.CharField(max_length=255, null=True, blank=True)
    detail = models.CharField(max_length=255, null=True, blank=True)
    favorite = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Diary(models.Model):
    time = models.DateTimeField()
    mood = models.ManyToManyField(FactorDetail, related_name='mood')
    place = models.CharField(max_length=255, null=True, blank=True)
    weather = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    people = models.ManyToManyField(FactorDetail, related_name='people')

    def __str__(self) -> str:
        return f'Diary at {self.time}'


class SleepTimeField(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    day = models.DateField(null=False, blank=False)
    hour = models.DecimalField(null=False, blank=False, max_digits=2, decimal_places=1)

    def __str__(self) -> str:
        return f'{self.day} sleep {self.hour} hour'


class UserDiary(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    diary = models.ManyToManyField(Diary)
    factor = models.ManyToManyField(FactorDetail)
    sleep_time = models.ManyToManyField(SleepTimeField)

    def __str__(self) -> str:
        return f'User diary name: {self.user}'
