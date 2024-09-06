from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('attestationJ/', views.AttestationJView.as_view(), name='att'),
    path('CertifiedValueJ', views.CertifiedValueJView.as_view(), name='cv'),
    path('equipment/', views.EquipmentView.as_view(), name='eq'),
    path('attjreg/', views.attestationJRegView, name='attjreg'),
    path('about/', views.About.as_view(), name='about'),
    path('contacts/', views.Contacts.as_view(), name='contacts'),
      ]

