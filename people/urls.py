from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^wall/$', views.wall, name='wall'),
    url(r'^success/$', views.success, name='success'),
]