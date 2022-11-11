from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('mood', views.mood, name='mood'),
    path('mood/sleep_time', views.set_sleep_time, name='set_sleep_time'),
    path('mood/record', views.record, name='record'),
    path('mood/views/<int:id>', views.view_mood, name='view_mood'),
    path('mood/accept/sleep_time', views.accept_sleep_time, name='accept_sleep_time'),
    path('mood/accept/adding', views.accept_adding, name='accept_adding'),
    path('mood/add_place', views.add_place, name='add_place'),
    path('mood/add_people', views.add_people, name='add_people'),
    path('mood/add_mood/list', views.add_mood_list, name='add_mood_list'),
    path('mood/dailymood', views.daily_mood, name='daily_mood'),
    path('mood/dailymood/show', views.daily_mood_show, name='daily_mood_show'),
    path('mood/discover', views.discover, name='discover'),
    path('mood/profile', views.profile, name='profile'),
]
