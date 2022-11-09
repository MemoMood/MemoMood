from django.urls import path
from . import views

urlpatterns = [
    # path('', views.welcome, name='welcome'),
    path('mood', views.mood, name='mood'),
    path('mood/record', views.record, name='record'),
    path('mood/accept/record', views.accept_record, name='accept_record'),
    path('mood/dailymood', views.daily_mood, name='dailymood'),
    path('mood/discover', views.discover, name='discover'),
    path('mood/profile', views.profile, name='profile'),
    path('mood/add_place', views.add_place, name='add_place'),
    path('mood/add_people', views.add_people, name='add_people'),
]
