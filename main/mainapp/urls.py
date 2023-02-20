from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('tristen_a3p3/', views.tristen_a3p3, name='tristena3p3'),
]