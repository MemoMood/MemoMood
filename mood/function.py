from mood.models import *
from django.shortcuts import get_object_or_404


def delete_mood(request, id):
    user = UserDiary.objects.get(user=request.user)
    diary = get_object_or_404(Diary, pk=id)
    user.diary.remove(diary)


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

def remove_factor(request, remove_list):
    user_diary = UserDiary.objects.get(user=request.user)
    for remove in remove_list:
        remove_item = FactorDetail.objects.get(name=remove)
        user_diary.factor.remove(remove_item)