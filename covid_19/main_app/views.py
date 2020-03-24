import os
from django.shortcuts import render
from .api.api import *
from .api.regression import *
from django.http import HttpResponse
import time
import shutil
import os

# Create your views here.
class GraphFile:
    POLYNOMIAL_DEGREE_THRESHOLD = 20
    MINIMUM_NUMBER_OF_DATAPOINTS = 5

    shouldFetchCountries=False
    LIMIT_COUNTRIES=5

    TOTAL_CASES="_TOTAL_CASES.png"
    TOTAL_CRITICAL="_TOTAL_CRITICAL.png"
    TOTAL_DEATHS="_TOTAL_DEATHS.png"
    TOTAL_RECOVERED="_TOTAL_RECOVERED.png"
    latest_path="graphs_latest/"
    stable_path="graphs_stable/"
    graph_image_store_path="main_app/static/main_app/images/"+latest_path
    graph_image_load_path="main_app/static/main_app/images/"+stable_path

def run_db_scripts(request):
    populate_db(GraphFile.LIMIT_COUNTRIES, GraphFile.shouldFetchCountries)
    return HttpResponse("Done")

def update_charts(request):
    countries = Country.objects.all()

    for c in countries:
        total=TotalCasesData.objects.filter(country=c)
        x=list()
        y=list()
        degree = 2 if total.count() < GraphFile.POLYNOMIAL_DEGREE_THRESHOLD else 3

        if total.count() > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            for item in total:
                x.append(int(time.mktime(item.record_date.timetuple())))
                y.append(item.total_cases)
                file_name = os.path.join(os.path.abspath(GraphFile.graph_image_store_path),c.country_name+GraphFile.TOTAL_CASES)
                regressionNumpy(x,y,degree,file_name,lineColor="peru", pointColor="sienna", ylabel="Total Infected")
        else:
            print("Not Enough Data")

        total=TotalDeathsData.objects.filter(country=c)
        x=list()
        y=list()
        degree = 2 if total.count() < GraphFile.POLYNOMIAL_DEGREE_THRESHOLD else 3

        if total.count() > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            for item in total:
                x.append(int(time.mktime(item.record_date.timetuple())))
                y.append(item.total_deaths)
                file_name = os.path.join(os.path.abspath(GraphFile.graph_image_store_path),c.country_name+GraphFile.TOTAL_DEATHS)
                regressionNumpy(x,y,degree,file_name,lineColor="tomato", pointColor="tab:red", ylabel="Total Deaths")

        else:
            print("Not Enough Data")

        total=TotalRecoveredData.objects.filter(country=c)
        x=list()
        y=list()
        degree = 2 if total.count() < GraphFile.POLYNOMIAL_DEGREE_THRESHOLD else 3
        if total.count() > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            for item in total:
                x.append(int(time.mktime(item.record_date.timetuple())))
                y.append(item.total_recovered)
                file_name = os.path.join(os.path.abspath(GraphFile.graph_image_store_path),c.country_name+GraphFile.TOTAL_RECOVERED)
                regressionNumpy(x,y,degree,file_name,lineColor="lightgreen", pointColor="tab:green", ylabel="Total Recovered")

        else:
            print("Not Enough Data")

        total=TotalCriticalData.objects.filter(country=c)
        x=list()
        y=list()
        degree = 2 if total.count() < GraphFile.POLYNOMIAL_DEGREE_THRESHOLD else 3
        if total.count() > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            for item in total:
                x.append(int(time.mktime(item.record_date.timetuple())))
                y.append(item.total_critical)
                file_name = os.path.join(os.path.abspath(GraphFile.graph_image_store_path),c.country_name+GraphFile.TOTAL_CRITICAL)
                regressionNumpy(x,y,degree,file_name,lineColor="plum", pointColor="rebeccapurple", ylabel="Total Critical")
        else:
            print("Not Enough Data")

    return HttpResponse("Done")

def view_latest_charts(request):
    prefix = GraphFile.latest_path
    countries = Country.objects.all()

    data = dict()

    for c in countries:

        country_flag = get_country_flag(c.country_name)
        graphs = list()

        count = TotalCasesData.objects.filter(country=c).count()
        if count >= GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_CASES)

        count = TotalCriticalData.objects.filter(country=c).count()
        if count >= GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_CRITICAL)

        count = TotalDeathsData.objects.filter(country=c).count()
        if count >= GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_DEATHS)

        count = TotalRecoveredData.objects.filter(country=c).count()
        if count >= GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_RECOVERED)

        data[c.country_name] = (country_flag,graphs)

    return render(request,"main_app/index.html", context={"data":data})

def move_latest_chart_to_stable(request):
    source = os.path.join(os.path.abspath(GraphFile.graph_image_store_path))+"/"
    dest1 = os.path.join(os.path.abspath(GraphFile.graph_image_load_path))+"/"

    files = os.listdir(source)

    for f in files:
        shutil.move(source+f, dest1+f)

    return HttpResponse("Done")

def home(request):
    prefix = GraphFile.stable_path
    countries = Country.objects.all()

    data = dict()

    for c in countries:

        country_flag = get_country_flag(c.country_name)
        graphs = list()

        count = TotalCasesData.objects.filter(country=c).count()
        if count >= GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_CASES)
        #else: graphs.append(GraphFile.NOT_ENOUGH_DATA_IMAGE)

        count = TotalCriticalData.objects.filter(country=c).count()
        if count >= GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_CRITICAL)
        #else: graphs.append(GraphFile.NOT_ENOUGH_DATA_IMAGE)

        count = TotalDeathsData.objects.filter(country=c).count()
        if count >= GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_DEATHS)
        #else: graphs.append(GraphFile.NOT_ENOUGH_DATA_IMAGE)

        count = TotalRecoveredData.objects.filter(country=c).count()
        if count >= GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_RECOVERED)
        #else: graphs.append(GraphFile.NOT_ENOUGH_DATA_IMAGE)

        data[c.country_name] = (country_flag,graphs)

    return render(request,"main_app/index.html", context={"data":data})