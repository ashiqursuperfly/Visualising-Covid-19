from django.contrib import admin
from .models import *

# Register your models here
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'self.country_name')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'record_date', 'total_cases', 'total_deaths', 'total_critical', 'total_recovered')


admin.site.register(Country)
admin.site.register(Covid19Data)