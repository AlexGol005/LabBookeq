from django.urls import path


from . import views


urlpatterns = [
    path('oferta/', views.OfertaView.as_view(), name='oferta'),
    path('politycaconfident/', views.PolitycaConfidentView.as_view(), name='politycaconfident'),
    path('', views.RegstrView.as_view(), name='reg'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('manual/', views.ManualView.as_view(), name='manual'),
    ]
