from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_discover, name='index_discover'),
    path('place', views.mood_with_place, name='mood_with_place'),
]
