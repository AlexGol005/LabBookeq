from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('equipment/', views.EquipmentView.as_view(), name='eq'),
    path('contacts/', views.Contacts.as_view(), name='contacts'),
      ]

