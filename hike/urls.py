from django.urls import path

from . import views
from . import constants


urlpatterns = [
    path('', views.HikeAllListView.as_view(), name=URL + 'head'),
    ]
