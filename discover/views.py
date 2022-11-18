from django.shortcuts import render, HttpResponse
from mood.models import MoodFactors, FactorDetail, SleepTimeField, Diary

# Create your views here.
def index_discover(request):
    return render(request, 'discover/index.html')

def mood_with_place(request):
    return render(request, 'discover/place.html')

def mood_with_sleep_time(request):
    return render(request, 'discover/sleep_time.html')