from django.shortcuts import render, HttpResponse

# Create your views here.
def index_discover(request):
    return render(request, 'discover/index.html')