from django.db import models

# Create your models here.


class MoodFactors(models.Model):
    factor = models.CharField(
        max_length=255, unique=True, null=False, blank=False)

    def __str__(self) -> str:
        return self.factor


class FactorDetail(models.Model):
    factor = models.ForeignKey(MoodFactors, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True,
                            null=False, blank=False)

    def __str__(self) -> str:
        return self.name


class Diary(models.Model):
    time = models.DateTimeField(blank=False, null=False)
    mood = models.CharField(max_length=255, blank=False, null=False)
    place = models.CharField(max_length=255, blank=False, null=False)
    weather = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=True, null=True)
    people = models.ManyToManyField(FactorDetail)

    def __str__(self) -> str:
        return f'Diary at {self.time}'


class SleepTimeField(models.Model):
    day = models.DateField(null=False, blank=False)
    hour = models.DecimalField(
        null=False, blank=False, max_digits=2, decimal_places=2)
