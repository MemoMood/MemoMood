from django.db import models

# Create your models here.


class MoodFactors(models.Model):
    factor = models.CharField(
        max_length=255, unique=True, null=False, blank=False)

    def __str__(self) -> str:
        return self.factor


class Detail(models.Model):
    factor = models.ForeignKey(MoodFactors, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)

    def __str__(self) -> str:
        return self.name


class TimeSelection(models.Model):
    start = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    end = models.DateTimeField(blank=True, null=True)

    def duration(self):
        if not self.end:
            return 0
        return self.end - self.start


class Diary(models.Model):
    text = models.TextField()
