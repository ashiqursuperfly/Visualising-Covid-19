from django.shortcuts import render
from .api.api import *
from .api.regression import *
from django.http import HttpResponse
import time
# Create your views here.

def run_db_scripts(request):
    populate_db()
    return HttpResponse("Done")

def update_charts(request):
    countries = Country.objects.all()
    for c in countries:

        total=TotalCasesData.objects.filter(country=c)
        x=list()
        y=list()
        for item in total:
            x.append(int(time.mktime(item.record_date.timetuple())))
            y.append(item.total_cases)
            regressionNumpy(x,y,3,c.country_name+"_TOTAL_CASES",lineColor="peru", pointColor="sienna", ylabel="Total Infected")

        total=TotalDeathsData.objects.filter(country=c)
        x=list()
        y=list()
        for item in total:
            x.append(int(time.mktime(item.record_date.timetuple())))
            y.append(item.total_deaths)
            regressionNumpy(x,y,3,c.country_name+"_TOTAL_DEATHS",lineColor="tomato", pointColor="tab:red", ylabel="Total Deaths")

        total=TotalRecoveredData.objects.filter(country=c)
        x=list()
        y=list()
        for item in total:
            x.append(int(time.mktime(item.record_date.timetuple())))
            y.append(item.total_recovered)
            regressionNumpy(x,y,3,c.country_name+"_TOTAL_RECOVERED",lineColor="lightgreen", pointColor="tab:green", ylabel="Total Recovered")

        total=TotalCriticalData.objects.filter(country=c)
        x=list()
        y=list()
        for item in total:
            x.append(int(time.mktime(item.record_date.timetuple())))
            y.append(item.total_critical)
            regressionNumpy(x,y,3,c.country_name+"_TOTAL_CRITICAL",lineColor="plum", pointColor="tab:purple", ylabel="Total Critical")


    return HttpResponse("Done")


