from django.urls import path

from . import views


urlpatterns = [
    path('bdanswer/<str:str>/', views.BdanswersQestionView.as_view(), name='bdanswer'),
    path('bdanswersall/', views.BdanswersAll.as_view(), name='bdanswersall'),
    path('searchresult/', views.SearchResultView.as_view(), name='bdanswerssearchresult'),
    path('bdanswerslist/', views.BdanswersListView.as_view(), name='bdanswerslist'),
    ]
