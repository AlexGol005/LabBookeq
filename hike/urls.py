from django.urls import path

from . import views
from . constants import *


urlpatterns = [
    path('', views.HikeAllListView.as_view(), name=URL + 'head'),
    path('bm', views.BMAllListView.as_view(), name='bm'),
    path('it', views.ITAllListView.as_view(), name='it'),
    path('it/searchresult/', views.ITSearchResultView.as_view(), name='itsearchresult'),
    path('<int:pk>/', views.HikeStrView.as_view(), name='hikestr'),
    path('hike/searchresult/', views.SearchResultView.as_view(), name='hikesearchresult'),
    path('filter/<int:pk>', views.filterview, name='bmfilter'),
    ]
