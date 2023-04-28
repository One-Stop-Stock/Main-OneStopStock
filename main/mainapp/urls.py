from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
]