from django.contrib import admin
from django.urls import path, include
from main_app import views

urlpatterns = [
    path('view_latest_charts', views.view_latest_charts, ''),
    path('', views.home, name="home"),
]