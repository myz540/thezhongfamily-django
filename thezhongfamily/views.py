from django.shortcuts import render
from django.http import HttpResponse, Http404
from datetime import datetime, timedelta

# Create your views here.
def index(request):
    return render(request, 'home.html')


def time(request):
    time = datetime.now()
    response = "<h1>The current date/time is: %s </h1>" % time
    return HttpResponse(response)


def plus_hours(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.now() + timedelta(hours=offset)
    response = "<h1>In %s hours, it will be %s</h1>" % (offset, dt)
    return HttpResponse(response)