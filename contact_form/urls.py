from django.contrib import admin
from django.urls import path
from contact_form.views import ContactForm, success, ContactCreate

urlpatterns = [
    path('', ContactCreate.as_view(), name='contact_page'),
    path('success/', success, name='success_page')
]