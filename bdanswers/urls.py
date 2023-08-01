from django.urls import path

from . import views


urlpatterns = [
    # path('', views.BdanswersView.as_view(), name='bdanswers'),
    # path('', views.BdanswersRegView.as_view(), name='bdanswersreg'),
    path('bdquestion/<str:str>/', views.BdanswersQestionView.as_view(), name='bdquestion'),
    path('bdanswersall/', views.BdanswersAll.as_view(), name='bdanswersall'),
    ]
