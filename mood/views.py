from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from mood.models import Diary, FactorDetail, MoodFactors

# Create your views here.


def welcome(request):
    return render(request, 'mood/welcome.html')


def mood(request):
    time_now = timezone.now()
    before_24 = time_now - timedelta(hours=23, minutes=59, seconds=59)
    try:
        diary_get = Diary.objects.filter(
            time__range=[before_24, time_now]).order_by("-time")
    except Diary.DoesNotExist:
        diary_get = []
    dict_return = {'diary': diary_get}
    return render(request, 'mood/index.html', dict_return)


def set_sleep_time(request):
    return render(request, 'mood/sleep_time.html',)


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
    if request.POST:
        time = request.POST.get('record-time')
        datetime_object = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        place = request.POST.get('place-input')
        weather = request.POST.get('weather-input')
        people = request.POST.getlist('friends-name[]')
        text = request.POST.get('text-input')
        # add to diary
        diary = Diary()
        diary.time = datetime_object
        diary.place = place
        diary.weather = weather
        diary.text = text
        diary.save()
        for p in people:
            find_name = FactorDetail.objects.get(name=p)
            diary.people.add(find_name)
        diary.save()
        return HttpResponseRedirect(reverse('accept_record'))
    time_format = timezone.now().strftime(f"%Y-%m-%dT%H:%M")
    dict_return = {'time': time_format,
                   'places': places_list, 'peoples': peoples_list}
    return render(request, 'mood/record.html', dict_return)


def add_place(request):
    if request.POST:
        place = request.POST.get('new-place')
        places = MoodFactors.objects.get(factor='place')
        places_list = [str(p) for p in places.factordetail_set.all()]
        if place not in places_list:
            places.factordetail_set.create(name=place)
        return HttpResponseRedirect(reverse('accept_place'))
    return render(request, 'mood/add_choice/add_place.html')


def add_people(request):
    if request.POST:
        people = request.POST.getlist('new-friend')
        peoples = MoodFactors.objects.get(factor='people')
        peoples_list = [str(p) for p in peoples.factordetail_set.all()]
        for i in people:
            if i not in peoples_list:
                peoples.factordetail_set.create(name=i)
        return HttpResponseRedirect(reverse('accept_people'))
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
    return render(request, 'mood/profile.html')
