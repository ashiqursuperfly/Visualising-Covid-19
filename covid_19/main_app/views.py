import os
from django.shortcuts import render
from .api.api import *
from .api.regression import *
from django.http import HttpResponse
import time
# Create your views here.

class GraphFile:
    TOTAL_CASES="_TOTAL_CASES"
    TOTAL_CRITICAL="_TOTAL_CRITICAL"
    TOTAL_DEATHS="_TOTAL_DEATHS"
    TOTAL_RECOVERED="_TOTAL_RECOVERED"
    graph_image_store_path="main_app/static/main_app/images"



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
            file_name = os.path.join(os.path.abspath(GraphFile.graph_image_store_path),c.country_name+GraphFile.TOTAL_CASES+".png")
            regressionNumpy(x,y,3,file_name,lineColor="peru", pointColor="sienna", ylabel="Total Infected")

        total=TotalDeathsData.objects.filter(country=c)
        x=list()
        y=list()
        for item in total:
            x.append(int(time.mktime(item.record_date.timetuple())))
            y.append(item.total_deaths)
            file_name = os.path.join(os.path.abspath(GraphFile.graph_image_store_path),c.country_name+GraphFile.TOTAL_DEATHS+".png")
            regressionNumpy(x,y,3,file_name,lineColor="tomato", pointColor="tab:red", ylabel="Total Deaths")

        total=TotalRecoveredData.objects.filter(country=c)
        x=list()
        y=list()
        for item in total:
            x.append(int(time.mktime(item.record_date.timetuple())))
            y.append(item.total_recovered)
            file_name = os.path.join(os.path.abspath(GraphFile.graph_image_store_path),c.country_name+GraphFile.TOTAL_RECOVERED+".png")
            regressionNumpy(x,y,3,file_name,lineColor="lightgreen", pointColor="tab:green", ylabel="Total Recovered")

        total=TotalCriticalData.objects.filter(country=c)
        x=list()
        y=list()
        for item in total:
            x.append(int(time.mktime(item.record_date.timetuple())))
            y.append(item.total_critical)
            file_name = os.path.join(os.path.abspath(GraphFile.graph_image_store_path),c.country_name+GraphFile.TOTAL_CRITICAL+".png")
            regressionNumpy(x,y,3,file_name,lineColor="plum", pointColor="rebeccapurple", ylabel="Total Critical")


    return HttpResponse("Done")

def home(request):
    countries = Country.objects.all()
    
    data = dict()
    
    for c in countries:
        graphs = list()
        graphs.append(c.country_name+GraphFile.TOTAL_CASES)
        graphs.append(c.country_name+GraphFile.TOTAL_CRITICAL)
        graphs.append(c.country_name+GraphFile.TOTAL_DEATHS)
        graphs.append(c.country_name+GraphFile.TOTAL_RECOVERED)
        data[c.country_name] = graphs

    return render(request,"main_app/index.html", context=data)