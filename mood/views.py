from datetime import datetime
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from mood.models import Diary, FactorDetail, MoodFactors

# Create your views here.


def mood(request):
    return render(request, 'mood/index.html')


def record(request):
    if not MoodFactors.objects.all():
        place_factors = MoodFactors(factor='place')
        place_factors.save()
        people_factors = MoodFactors(factor='people')
        people_factors.save()
        mood_factors = MoodFactors(factor='mood')
        mood_factors.save()
    places = MoodFactors.objects.get(factor='place')
    peoples = MoodFactors.objects.get(factor='people')
    places_list = [str(p) for p in places.factordetail_set.all()]
    peoples_list = [str(p) for p in peoples.factordetail_set.all()]
    time_format = timezone.now().strftime(f"%Y-%m-%dT%H:%M")
    dict_return = {'time': time_format,
                   'places': places_list, 'peoples': peoples_list}
    return render(request, 'mood/record.html', dict_return)


def add_place(request):
    return render(request, 'mood/add_choice/add_place.html')


def add_people(request):
    return render(request, 'mood/add_choice/add_people.html')


def accept_record(request):
    return render(request, 'mood/accept_components/back_from_record.html')


def accept_place(request):
    return render(request, 'mood/accept_components/back_from_place.html')


def accept_people(request):
    return render(request, 'mood/accept_components/back_from_people.html')


def daily_mood(request):
    return render(request, 'mood/daily_mood.html')


def discover(request):
    return render(request, 'mood/discover.html')


def profile(request):
    return render(request, 'dashboard/home.html')
