from django.urls import path

from . import views
from . import constants


urlpatterns = [
    path('', views.Head.as_view(), name=URL + 'head'),
    ]
