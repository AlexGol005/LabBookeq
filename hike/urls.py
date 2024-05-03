from django.urls import path

from . import views


urlpatterns = [
    path('', views.Head.as_view(), name=URL + 'head'),
    ]
