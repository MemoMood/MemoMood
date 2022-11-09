from django.contrib import admin
from .models import MoodFactors, FactorDetail, Diary, SleepTimeField

# Register your models here.
admin.site.register(MoodFactors)
admin.site.register(FactorDetail)
admin.site.register(Diary)
admin.site.register(SleepTimeField)