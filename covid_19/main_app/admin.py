from django.contrib import admin
from .models import *

# Register your models here
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name','continent_id', 'code')

class TotalCasesAdmin(admin.ModelAdmin):
    list_display = ('country', 'record_date', 'total_cases')

class TotalRecoveredAdmin(admin.ModelAdmin):
    list_display = ('country', 'record_date', 'total_recovered')

class TotalDeathsAdmin(admin.ModelAdmin):
    list_display = ('country', 'record_date', 'total_deaths')

class TotalCriticalAdmin(admin.ModelAdmin):
    list_display = ('country', 'record_date', 'total_critical')

class EstimatedTotalCasesAdmin(admin.ModelAdmin):
    list_display = ('country', 'estimated_date', 'estimated_total_cases', 'estimated_new_cases')

admin.site.register(Country, CountryAdmin)
admin.site.register(TotalCasesData, TotalCasesAdmin)
admin.site.register(TotalRecoveredData, TotalRecoveredAdmin)
admin.site.register(TotalCriticalData, TotalCriticalAdmin)
admin.site.register(TotalDeathsData, TotalDeathsAdmin)
admin.site.register(EstimatedTotalCasesData, EstimatedTotalCasesAdmin)

