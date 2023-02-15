from django.urls import path


from . import views


urlpatterns = [
    path('', views.BlogView.as_view(), name='blog'),
    path('<int:pk>/', views.BlogStrView.as_view(), name='blogstr'),
    ]
