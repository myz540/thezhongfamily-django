from django.shortcuts import render
from django.template import Context, Template
from django.http import Http404, HttpResponse

# Create your views here.

def index(request):
    context = {'var': 'var'}
    return render(request, "catan/catan.html", context)


def sim(request):
    return HttpResponse("Game Simulation")
