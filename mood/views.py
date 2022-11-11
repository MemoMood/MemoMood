from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from mood.models import Diary, FactorDetail, MoodFactors, SleepTimeField

# Create your views here.


def check_null():
    if not MoodFactors.objects.all():
        place_factors = MoodFactors(factor='place')
        place_factors.save()
        people_factors = MoodFactors(factor='people')
        people_factors.save()
        mood = MoodFactors(factor='mood')
        mood.save()


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


def view_mood(request, id):
    diary = get_object_or_404(Diary, pk=id)
    dict_return = {'diary': diary}
    return render(request, 'mood/view_mood.html', dict_return)


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
    moods = MoodFactors.objects.get(factor='mood')
    places_list = [str(p) for p in places.factordetail_set.all()]
    peoples_list = [str(p) for p in peoples.factordetail_set.all()]
    positive_moods_list = [str(m)
                           for m in moods.factordetail_set.all() if m.category == 'Positive' and m.favorite]
    negative_moods_list = [str(m)
                           for m in moods.factordetail_set.all() if m.category == 'Negative' and m.favorite]
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
    check_null()
    if request.POST:
        place = request.POST.get('new-place')
        place = place.lower()
        places = MoodFactors.objects.get(factor='place')
        places_list = [str(p) for p in places.factordetail_set.all()]
        if place not in places_list:
            places.factordetail_set.create(name=place)
        return HttpResponseRedirect(reverse('record'))
    return render(request, 'mood/add_choice/add_place.html')


def add_people(request):
    check_null()
    if request.POST:
        people = request.POST.getlist('new-friend')
        peoples = MoodFactors.objects.get(factor='people')
        peoples_list = [str(p) for p in peoples.factordetail_set.all()]
        for i in people:
            if i not in peoples_list:
                i = i.lower()
                peoples.factordetail_set.create(name=i)
        return HttpResponseRedirect(reverse('record'))
    return render(request, 'mood/add_choice/add_people.html')


def add_mood_list(request):
    mood_obj = MoodFactors.objects.get(factor='mood')
    with open('mood/static/mood/moodwheel.txt') as f:
        lines = [line.rstrip() for line in f]
    if not mood_obj.factordetail_set.all():
        for line in lines:
            mood = line.split(',')
            if len(mood) == 3:
                mood_obj.factordetail_set.create(name=mood[2])
                mood_fac = FactorDetail.objects.get(name=mood[2])
                mood_fac.category = mood[0]
                mood_fac.detail = mood[1]
                mood_fac.save()
    if request.POST:
        fav_list = request.POST.getlist('fav-mood[]')
        print(fav_list)
        for fav in fav_list:
            fav_obj = FactorDetail.objects.get(name=fav)
            fav_obj.favorite = True
            fav_obj.save()
        return HttpResponseRedirect(reverse('record'))
    dict_return = {}
    detail_list = ['Main', 'Joyful', 'Powerful', 'Peaceful', 'Sad', 'Mad', 'Scared']
    for detail in detail_list:
        detail_obj_list = [str(m) for m in MoodFactors.objects.get(
            factor='mood').factordetail_set.all() if m.detail == detail]
        dict_return[detail] = detail_obj_list
    return render(request, 'mood/add_choice/mood_list.html', dict_return)


def accept_sleep_time(request):
    return render(request, 'mood/accept_components/back_from_sleep_time.html')


def accept_adding(request):
    return render(request, 'mood/accept_components/back_home_record.html')


def daily_mood(request):
    return render(request, 'mood/daily_mood.html')


def daily_mood_show(request):
    return render(request, 'mood/daily_mood_show.html')


def discover(request):
    moods = MoodFactors.objects.get(factor='mood')
    mood_list = [str(m) for m in moods.factordetail_set.all()]
    dict_return = {"mood": mood_list}
    if request.POST:
        selected_mood = request.POST.get('select-mood')
        print(selected_mood)
        discover_sleep = []
        return render(request, 'mood/discover.html', dict_return)
    return render(request, 'mood/discover.html', dict_return)


def profile(request):
    return render(request, 'mood/profile.html')
