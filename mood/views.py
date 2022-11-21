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


def check_mood_null():
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


def old_mood(request):
    if request.POST:
        user_diary = UserDiary.objects.get(user=request.user)
        diary_user = user_diary.diary.all()
        date = request.POST.get('show-time')
        datetime_min = datetime.strptime(date, '%Y-%m-%d')
        datetime_max = datetime_min + timedelta(hours=23, minutes=59, seconds=59)
        sorted_user_diary = diary_user.filter(time__range=[datetime_min, datetime_max])
        return render(request, 'mood/mood_sort.html', {'diary': sorted_user_diary, 'select_time': date})
    diary = {}
    return render(request, 'mood/mood_sort.html', diary)


def view_mood(request, id):
    diary = get_object_or_404(Diary, pk=id)
    dict_return = {'diary': diary}
    return render(request, 'mood/view_mood.html', dict_return)


def set_sleep_time(request):
    if not request.user.is_authenticated:
        return redirect('profile')
    if request.POST:
        user_diary = UserDiary.objects.get(user=request.user)
        sleep_time_user = user_diary.sleep_time.all()
        date = request.POST.get('record-time')
        datetime_object = datetime.strptime(date, '%Y-%m-%d').date()
        sleep_time = request.POST.get('sleep-time-input')
        try:
            sleep_time_get_obj = sleep_time_user.get(
                day=datetime_object)
        except SleepTimeField.DoesNotExist:
            sleep_time_get_obj = None
        if not sleep_time_get_obj:
            sleep_time_obj = SleepTimeField(user=request.user)
            sleep_time_obj.day = datetime_object
            sleep_time_obj.hour = float(sleep_time)
            sleep_time_obj.save()
            user_diary.sleep_time.add(sleep_time_obj)
        else:
            sleep_time_get_obj.hour = float(sleep_time)
            sleep_time_get_obj.save()
        return HttpResponseRedirect(reverse('accept_sleep_time'))
    time_format = timezone.now().strftime(f"%Y-%m-%d")
    dict_return = {'time': time_format}
    return render(request, 'mood/sleep_time.html', dict_return)


@login_required
def record(request):
    check_null()
    check_mood_null()
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
    check_mood_null()
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
    check_mood_null()
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
    check_mood_null()
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


def get_percent_in_week(request,week_start):
    user_obj = UserDiary.objects.get(user=request.user)
    user_diary = user_obj.diary.all()
    week_date = {}
    count_mood_pos = {}
    count_mood_neg = {}
    for i in range(0, 7, 1):
        some_day = week_start + timedelta(days=i)
        week_date[some_day.weekday()] = some_day
    for key, j in week_date.items():
        count_pos = user_diary.filter(time__gte=j, time__lte=j+timedelta(days=1), mood__category="Positive").count()
        count_neg = user_diary.filter(time__gte=j, time__lte=j+timedelta(days=1), mood__category="Negative").count()
        count_mood_pos[key], count_mood_neg[key] = count_pos, count_neg
    value_for_graph = []
    for k in range(0, 7, 1):
        positive_count = count_mood_pos[k]
        all_count = count_mood_pos[k] + count_mood_neg[k]
        if all_count == 0:
            percent_positive = 0
        else:
            percent_positive = positive_count/all_count*100
        value_for_graph.append(percent_positive)
    return value_for_graph


def daily_mood(request):
    time_now = timezone.now().strftime(f"%Y-W%V")
    if request.POST:
        week = request.POST.get('choose-week')
        datetime_object = datetime.strptime(week + '-1', '%G-W%V-%u')
        datetime_object_7 = datetime_object + timedelta(days=6, hours=23, minutes=59, seconds=59)
        percent = get_percent_in_week(request, datetime_object)
        str_week = str(datetime_object.date())+ " to " + str(datetime_object_7.date())
        dict_return = {'percent': percent, 'time_max': time_now, 'week': week, 'week_str': str_week}
        return render(request, 'mood/daily_mood.html', dict_return)
    return render(request, 'mood/daily_mood.html', {'percent': [], 'time_max': time_now,'week_str': 'choose a week'})


def daily_mood_show(request):
    return render(request, 'mood/daily_mood_show.html')


def discover(request):
    check_null()
    check_mood_null()
    user = request.user
    moods = MoodFactors.objects.get(factor='mood')
    places = MoodFactors.objects.get(factor='place')
    places_list_all = [str(p) for p in places.factordetail_set.all()]
    mood_list_all = [str(m) for m in moods.factordetail_set.all()]
    dict_return = {"mood": mood_list_all, "place": places_list_all}
    try:
        user_diary_get = UserDiary.objects.get(user=request.user)
    except UserDiary.DoesNotExist:
        return redirect('profile')
    if request.POST:
        selected_mood = request.POST.get('select-mood')
        dict_return['select'] = selected_mood
        user_factor = user_diary_get.diary.all()
        sort_diary_mood = user_factor.filter(mood__name=selected_mood)

        # place
        top_place = count_place(sort_diary_mood)
        dict_return['top_place'] = top_place

        # people
        top_people = count_people(sort_diary_mood)
        dict_return['top_people'] = top_people

        # weather
        count_weather = weather_prep(sort_diary_mood)
        dict_return['weather'] = list(count_weather.values())

        # sleep_time
        count_sleep_hour, avg_sleep = sleep_time_prep(
            user_diary_get, sort_diary_mood)
        dict_return['sleep_hour'] = list(count_sleep_hour.values())

        # average sleep time
        dict_return['avg_sleep'] = avg_sleep

        return render(request, 'mood/discover.html', dict_return)
    return render(request, 'mood/discover.html', dict_return)


def count_place(sort_diary_mood):
    count_place = {}
    for i in sort_diary_mood:
        if i.place not in count_place:
            count_place[i.place] = 1
        else:
            count_place[i.place] += 1
    count_place = dict(
        sorted(count_place.items(), key=lambda item: item[1], reverse=True))
    key_place = list(count_place.keys())
    len_key_place = len(key_place)
    if len_key_place < 3:
        for i in range(3-len_key_place):
            key_place.append('')
    else:
        key_place = key_place[:3]
    return key_place


def count_people(sort_diary_mood):
    count_people = {}
    for i in sort_diary_mood:
        for j in i.people.all():
            if j.name not in count_people:
                count_people[j.name] = 1
            else:
                count_people[j.name] += 1
    count_people = dict(sorted(count_people.items(),
                        key=lambda item: item[1], reverse=True))
    key_people = list(count_people.keys())
    len_key_people = len(key_people)
    if len_key_people < 3:
        for i in range(3-len_key_people):
            key_people.append('')
    else:
        key_people = key_people[:3]
    return key_people


def weather_prep(sort_diary_mood):
    count_weather = {"sunny": 0, "cloudy": 0, "rainny": 0,
                     "thunderstorm": 0, "foggy": 0, "snow": 0}
    for i in sort_diary_mood:
        count_weather[i.weather] += 1
    return count_weather


def sleep_time_prep(user_diary, sort_diary_mood):
    sleep_time = []
    mood_date_list = [mood.time.date() for mood in sort_diary_mood]
    result_sleep_time = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0,
                         "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0}
    sleep_time_get = user_diary.sleep_time.all()
    for date in mood_date_list:
        try:
            date_with_hour = sleep_time_get.get(day=date)
            sleep_time.append(date_with_hour.hour)
            result_sleep_time[str(int(date_with_hour.hour))] += 1
        except SleepTimeField.DoesNotExist:
            pass
    if len(sleep_time) == 0:
        avg_sleep_time = 0
    else:
        avg_sleep_time = sum(sleep_time) / len(sleep_time)
    return result_sleep_time, avg_sleep_time


def profile(request):
    return render(request, 'dashboard/home.html')


def choose_category_remove(request):
    if request.POST:
        category = request.POST.get('choose-c')
        return render(request, 'mood/remove_choice/remove_factor.html', {'category': category})
    return render(request, 'mood/remove_choice/choose_category_remove.html')


def get_choice_list(request, category):
    user_diary = UserDiary.objects.get(user=request.user)
    mood_factor = MoodFactors.objects.get(factor=category)
    factor = user_diary.factor.filter(factor=mood_factor)
    return factor


def remove_factor(request, remove_list):
    user_diary = UserDiary.objects.get(user=request.user)
    for remove in remove_list:
        remove_item = FactorDetail.objects.get(name=remove)
        user_diary.factor.remove(remove_item)


def remove_mood(request):
    if not request.user.is_authenticated:
        return redirect('profile')
    if request.POST:
        remove_list = request.POST.getlist('remove-mood[]')
        remove_factor(request, remove_list)
        return redirect('record')
    factor = get_choice_list(request, 'mood')
    return render(request, 'mood/remove_choice/remove_mood.html', {'category': 'mood', 'factor': factor})


def remove_place(request):
    if not request.user.is_authenticated:
        return redirect('profile')
    if request.POST:
        remove_list = request.POST.getlist('remove-place[]')
        remove_factor(request, remove_list)
        return redirect('record')
    factor = get_choice_list(request, 'place')
    return render(request, 'mood/remove_choice/remove_place.html', {'category': 'place', 'factor': factor})


def remove_people(request):
    if not request.user.is_authenticated:
        return redirect('profile')
    if request.POST:
        remove_list = request.POST.getlist('remove-people[]')
        remove_factor(request, remove_list)
        return redirect('record')
    factor = get_choice_list(request, 'people')
    return render(request, 'mood/remove_choice/remove_people.html', {'category': 'people', 'factor': factor})
