from django.shortcuts import render

# Create your views here.


def welcome(request):
    return render(request, 'mood/welcome.html')

def mood(request):
    return render(request, 'mood/index.html')

def record(request):
    return render(request, 'mood/record.html')

def daily_mood(request):
    return render(request, 'mood/daily_mood.html')

def discover(request):
    return render(request, 'mood/discover.html')

def profile(request):
    return render(request, 'dashboard/home.html')
