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
    path('hikefilter/<int:pk>', views.hikefilterview, name='hikefilteryear'),
    path('donehikefilter/<int:qk>', views.donehikefilterview, name='donehikefilteryear'),
    path('readyhikefilter/<int:rk>', views.readyhikefilterview, name='readyhikefilteryear'),
    path('kareliahistory', views.KareliahistoryAllListView.as_view(), name='kareliahistory'),
    path('kareliahistory/searchresult/', views.KareliahistorySearchResultView.as_view(), name='kareliahistorysearchresult'),
    path('bm/searchresult/', views.BMSearchResultView.as_view(), name='bmsearchresult'),
    path('example', views.index, name='example'),
    #path('example', views.ExampleTemplateView.as_view(), name='example'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
