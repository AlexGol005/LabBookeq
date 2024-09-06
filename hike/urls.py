from django.urls import path

from . import views
from . constants import *


urlpatterns = [
    path('', views.HikeAllListView.as_view(), name=URL + 'head'),
    path('<int:pk>/', views.HikeStrView.as_view(), name='hikestr'),
    ]
