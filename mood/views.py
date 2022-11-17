from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from mood.models import Diary, FactorDetail, MoodFactors, SleepTimeField, UserDiary
from django.contrib.auth.decorators import login_required

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
    check_null()
    return render(request, 'mood/welcome.html')


def mood(request):
    time_now = timezone.now()
    before_24 = time_now - timedelta(hours=23, minutes=59, seconds=59)
    if not request.user.is_authenticated:
        return redirect('profile')
    try:
        user_diary_get = UserDiary.objects.get(user=request.user)
    except UserDiary.DoesNotExist:
        user_diary = UserDiary(user=request.user)
        user_diary.save()
    try:
        all_user_diary = user_diary_get.diary.all()
        sorted_user_diary = all_user_diary.filter(
            time__range=[before_24, time_now]).order_by("-time")
    except UnboundLocalError:
        sorted_user_diary = []
    dict_return = {'username': str(request.user), 'diary': sorted_user_diary}
    return render(request, 'mood/index.html', dict_return)


def view_mood(request, id):
    diary = get_object_or_404(Diary, pk=id)
    dict_return = {'diary': diary}
    return render(request, 'mood/view_mood.html', dict_return)


def set_sleep_time(request):
    if not request.user.is_authenticated:
        return redirect('profile')
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
            sleep_time_obj = SleepTimeField(user=request.user)
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


@login_required
def record(request):
    check_null()
    user = request.user
    if not user.is_authenticated:
        return redirect('profile')
    places = MoodFactors.objects.get(factor='place')
    peoples = MoodFactors.objects.get(factor='people')
    moods = MoodFactors.objects.get(factor='mood')
    try:
        user_diary_get = UserDiary.objects.get(user=request.user)
    except UserDiary.DoesNotExist:
        user_diary_get = UserDiary(user=request.user)
        user_diary_get.save()
    user_factor = user_diary_get.factor.all()
    places_list = user_factor.filter(factor=places)
    peoples_list = user_factor.filter(factor=peoples)
    moods_list = user_factor.filter(factor=moods)
    positive_moods_list = [str(m)
                           for m in moods_list if m.category == 'Positive']
    negative_moods_list = [str(m)
                           for m in moods_list if m.category == 'Negative']
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
        try:
            user_diary = UserDiary.objects.get(user=request.user)
        except UserDiary.DoesNotExist:
            user_diary = UserDiary(user=user)
            user_diary.save()
        user_diary.diary.add(diary)
        user_diary.save()
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
        user_diary_get = UserDiary.objects.get(user=request.user)
        place_user = user_diary_get.factor.all()
        places_object = MoodFactors.objects.get(factor='place')
        places_list = place_user.filter(factor=places_object)
        places_list_str = [str(p) for p in places_list]
        places_list_all = [str(p)
                           for p in places_object.factordetail_set.all()]
        if place.lower() not in places_list_str:
            place = place.lower()
            if place not in places_list_all:
                places_object.factordetail_set.create(name=place)
            find_place = FactorDetail.objects.get(name=place)
            user_diary_get.factor.add(find_place)
            user_diary_get.save()
        return HttpResponseRedirect(reverse('record'))
    return render(request, 'mood/add_choice/add_place.html')


def add_people(request):
    check_null()
    if request.POST:
        people = request.POST.getlist('new-friend')
        user_diary_get = UserDiary.objects.get(user=request.user)
        peoples_user = user_diary_get.factor.all()
        peoples_object = MoodFactors.objects.get(factor='people')
        peoples_list = peoples_user.filter(factor=peoples_object)
        peoples_list_str = [str(p) for p in peoples_list]
        peoples_list_all = [str(p)
                            for p in peoples_object.factordetail_set.all()]
        for i in people:
            i = i.lower()
            if i not in peoples_list_str:
                if i not in peoples_list_all:
                    peoples_object.factordetail_set.create(name=i)
                find_people = FactorDetail.objects.get(name=i)
                user_diary_get.factor.add(find_people)
                user_diary_get.save()
        return HttpResponseRedirect(reverse('record'))
    return render(request, 'mood/add_choice/add_people.html')


def add_mood_list(request):
    mood_obj = MoodFactors.objects.get(factor='mood')
    if not mood_obj.factordetail_set.all():
        with open('mood/static/mood/moodwheel.txt') as f:
            lines = [line.rstrip() for line in f]
        for line in lines:
            mood = line.split(',')
            if len(mood) == 3:
                mood_obj.factordetail_set.create(name=mood[2])
                mood_fac = FactorDetail.objects.get(name=mood[2])
                mood_fac.category = mood[0]
                mood_fac.detail = mood[1]
                mood_fac.save()
    if request.POST:
        user_diary_get = UserDiary.objects.get(user=request.user)
        user_factor = user_diary_get.factor.all()
        mood_object = MoodFactors.objects.get(factor='mood')
        moods_list = user_factor.filter(factor=mood_object)
        moods_list_str = [str(m) for m in moods_list]
        fav_list = request.POST.getlist('fav-mood[]')
        for fav in fav_list:
            if fav not in moods_list_str:
                fav_obj = FactorDetail.objects.get(name=fav)
                user_diary_get.factor.add(fav_obj)
                user_diary_get.save()
        return HttpResponseRedirect(reverse('record'))
    dict_return = {}
    detail_list = ['Main', 'Joyful', 'Powerful',
                   'Peaceful', 'Sad', 'Mad', 'Scared']
    for detail in detail_list:
        detail_obj_list = [str(m) for m in MoodFactors.objects.get(
            factor='mood').factordetail_set.all() if m.detail == detail]
        dict_return[detail] = detail_obj_list
    return render(request, 'mood/add_choice/mood_list.html', dict_return)


def accept_sleep_time(request):
    return render(request, 'mood/accept_components/back_from_sleep_time.html')


def accept_adding(request):
    return render(request, 'mood/accept_components/back_home_record.html')

def get_percent_in_week():
    week_date = {}
    count_mood_pos = {}
    count_mood_neg = {}
    for i in range(6, -1, -1):
        some_day = timezone.now().date() - timedelta(days=i)
        if some_day.weekday() == 6:
            week_date[0] = some_day
        else:
            week_date[some_day.weekday()+1] = some_day
    for key,j in week_date.items():
        count_pos = Diary.objects.filter(time__gte=j, time__lte=j+timedelta(days=1), mood__category="Positive").count()
        count_neg = Diary.objects.filter(time__gte=j, time__lte=j+timedelta(days=1), mood__category="Negative").count()
        count_mood_pos[key], count_mood_neg[key] = count_pos, count_neg
    count_mood_pos, count_mood_neg = dict(sorted(count_mood_pos.items())), dict(sorted(count_mood_neg.items()))
    value_for_graph = []
    for k in range(0, 7, 1):
        positive_count = count_mood_pos[k]
        all_count = count_mood_pos[k] + count_mood_neg[k]
        if all_count == 0:
            percent_positive = 0
        else:
            percent_positive = positive_count/all_count*100
        value_for_graph.append(percent_positive)
    week_date = dict(sorted(week_date.items()))
    week_date_list = week_date.values()
    return value_for_graph, week_date_list

def daily_mood(request):
    percent, week_date = get_percent_in_week()
    return render(request, 'mood/daily_mood.html', {'percent': percent})


def daily_mood_show(request):
    return render(request, 'mood/daily_mood_show.html')


def discover(request):
    return render(request, 'mood/discover.html')


def profile(request):
    return render(request, 'dashboard/home.html')
