from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_discover, name='index_discover')
]