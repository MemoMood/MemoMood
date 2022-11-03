from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from mood.models import Diary, FactorDetail, MoodFactors, SleepTimeField

# Create your views here.


def check_null():
    if not MoodFactors.objects.all():
        place_factors = MoodFactors(factor='place')
        place_factors.save()
        people_factors = MoodFactors(factor='people')
        people_factors.save()
        positive_mood = MoodFactors(factor='mood-positive')
        positive_mood.save()
        negative_mood = MoodFactors(factor='mood-negative')
        negative_mood.save()


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
    sleep_time_obj = SleepTimeField()
    if request.POST:
        date = request.POST.get('record-time')
        datetime_object = datetime.strptime(date, '%Y-%m-%d').date()
        sleep_time = request.POST.get('sleep-time-input')
        try:
            sleep_time_get_obj = SleepTimeField.objects.get(
                day=datetime_object)
        except SleepTimeField.DoesNotExist:
            sleep_time_get_obj = None
        if not sleep_time_get_obj:
            sleep_time_obj.day = datetime_object
            sleep_time_obj.hour = float(sleep_time)
            sleep_time_obj.save()
        else:
            keep_hour = sleep_time_get_obj.hour
            sleep_time_get_obj.hour = float(sleep_time)
            sleep_time_get_obj.save()
        return HttpResponseRedirect(reverse('accept_sleep_time'))
    time_format = timezone.now().strftime(f"%Y-%m-%d")
    dict_return = {'time': time_format}
    return render(request, 'mood/sleep_time.html', dict_return)


def record(request):
    check_null()
    places = MoodFactors.objects.get(factor='place')
    peoples = MoodFactors.objects.get(factor='people')
    positive_moods = MoodFactors.objects.get(factor='mood-positive')
    negative_moods = MoodFactors.objects.get(factor='mood-negative')
    places_list = [str(p) for p in places.factordetail_set.all()]
    peoples_list = [str(p) for p in peoples.factordetail_set.all()]
    positive_moods_list = [str(m)
                           for m in positive_moods.factordetail_set.all()]
    negative_moods_list = [str(m)
                           for m in negative_moods.factordetail_set.all()]
    if request.POST:
        time = request.POST.get('record-time')
        datetime_object = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        place = request.POST.get('place-input')
        weather = request.POST.get('weather-input')
        people = request.POST.getlist('friends-name[]')
        text = request.POST.get('text-input')
        mood = request.POST.getlist('mood-input[]')
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
        for m in mood:
            find_mood = FactorDetail.objects.get(name=m)
            diary.mood.add(find_mood)
        diary.save()
        return HttpResponseRedirect(reverse('accept_adding'))
    time_format = timezone.now().strftime(f"%Y-%m-%dT%H:%M")
    dict_return = {'time': time_format, 'places': places_list, 'peoples': peoples_list,
                   'positive_moods': positive_moods_list, 'negative_moods': negative_moods_list}
    return render(request, 'mood/record.html', dict_return)


def add_place(request):
    if request.POST:
        place = request.POST.get('new-place')
        places = MoodFactors.objects.get(factor='place')
        places_list = [str(p) for p in places.factordetail_set.all()]
        if place not in places_list:
            places.factordetail_set.create(name=place)
        return HttpResponseRedirect(reverse('accept_adding'))
    return render(request, 'mood/add_choice/add_place.html')


def add_people(request):
    if request.POST:
        people = request.POST.getlist('new-friend')
        peoples = MoodFactors.objects.get(factor='people')
        peoples_list = [str(p) for p in peoples.factordetail_set.all()]
        for i in people:
            if i not in peoples_list:
                peoples.factordetail_set.create(name=i)
        return HttpResponseRedirect(reverse('accept_adding'))
    return render(request, 'mood/add_choice/add_people.html')


def add_mood_positive(request):
    if request.POST:
        mood = request.POST.get('new-mood')
        mood_lower = mood.lower()
        moods = MoodFactors.objects.get(factor='mood-positive')
        positive_list = [str(m) for m in moods.factordetail_set.all()]
        if mood_lower not in positive_list:
            moods.factordetail_set.create(name=mood_lower)
        return HttpResponseRedirect(reverse('accept_adding'))
    return render(request, 'mood/add_choice/add_mood_positive.html',)


def add_mood_negative(request):
    check_null()
    if request.POST:
        mood = request.POST.get('new-mood')
        mood_lower = mood.lower()
        moods = MoodFactors.objects.get(factor='mood-negative')
        negative_list = [str(m) for m in moods.factordetail_set.all()]
        if mood_lower not in negative_list:
            moods.factordetail_set.create(name=mood_lower)
        return HttpResponseRedirect(reverse('record'))
    return render(request, 'mood/add_choice/add_mood_negative.html',)


def accept_sleep_time(request):
    return render(request, 'mood/accept_components/back_from_sleep_time.html')


def accept_adding(request):
    return render(request, 'mood/accept_components/back_home_record.html')


def daily_mood(request):
    return render(request, 'mood/daily_mood.html')


def daily_mood_show(request):
    return render(request, 'mood/daily_mood_show.html')


def discover(request):
    return render(request, 'mood/discover.html')


def profile(request):
    return render(request, 'dashboard/home.html')
