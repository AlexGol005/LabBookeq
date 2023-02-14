from django.urls import path
from django.contrib.auth.decorators import login_required


from . import views


urlpatterns = [
    path('', views.HeadView.as_view(), name='blog'),
    ]
# path('/search_location/result/', views.SearchResultView.as_view(), name=URL + 'search'),