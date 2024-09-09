from django.urls import path

from . import views
from . constants import *


urlpatterns = [
    path('', views.HikeAllListView.as_view(), name=URL + 'head'),
    path('bm', views.BMAllListView.as_view(), name='bm'),
    path('<int:pk>/', views.HikeStrView.as_view(), name='hikestr'),
    ]
