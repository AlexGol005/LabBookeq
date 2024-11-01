from django.urls import path


from . import views


urlpatterns = [
    path('', views.RegstrView.as_view(), name='reg'),
    path('about/', views.AboutView.as_view(), name='about'),
    ]
