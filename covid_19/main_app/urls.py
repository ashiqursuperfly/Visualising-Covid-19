from django.contrib import admin
from django.urls import path, include
from main_app import views

urlpatterns = [
    path('run_db_scripts', views.run_db_scripts, ''),
    path('update_charts', views.update_charts, ''),
    path('view_latest_charts', views.view_latest_charts, ''),
    path('move_latest_charts_to_stable', views.move_latest_chart_to_stable, ''),
    path('', views.home, name="home"),
]