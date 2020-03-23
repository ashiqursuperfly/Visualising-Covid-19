from django.contrib import admin
from django.urls import path, include
from main_app import views

urlpatterns = [
    path('run_db_scripts', views.run_db_scripts, ''),
    path('update_charts', views.update_charts, ''),
]