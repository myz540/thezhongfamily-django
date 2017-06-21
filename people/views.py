from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from people.models import *

# Create your views here.
def index(request):
    return render(request, "people/people.html")

def wall(request):
    context = {}
    recent_postings = WallPost.objects.order_by('-post_dt')[:5]

    if request.method == 'POST':
        print("post received")
        form = WallPostForm(request.POST)
        for k,v in request.POST.items():
            print(k, v, type(v))
        if form.is_valid() and form.is_bound:
            print("Valid and bound form")
            form.save()

    else:
        form = WallPostForm()

    context['form'] = form
    context['recent_postings'] = recent_postings
    return render(request, "people/wall.html", context)

def success(request):
    return render(request, "people/success.html")

