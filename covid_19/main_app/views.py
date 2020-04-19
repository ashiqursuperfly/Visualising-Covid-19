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
    POLYNOMIAL_DEGREE_THRESHOLD = 8
    MINIMUM_NUMBER_OF_DATAPOINTS = 10

    SHOULD_FETCH_COUNTRIES=False
    LIMIT_COUNTRIES=5

    TOTAL_CASES="_TOTAL_CASES.png"
    TOTAL_CRITICAL="_TOTAL_CRITICAL.png"
    TOTAL_DEATHS="_TOTAL_DEATHS.png"
    TOTAL_RECOVERED="_TOTAL_RECOVERED.png"

    latest_path="graphs_latest/"
    stable_path="graphs_stable/"
    pie="pie/"
    graph_image_store_path="main_app/static/main_app/images/"+latest_path
    graph_image_load_path="main_app/static/main_app/images/"+stable_path
    pie_store_path="main_app/static/main_app/images/"+pie

def view_latest_charts(request):
    prefix = GraphFile.latest_path
    countries = Country.objects.all().order_by('-continent_id')
    print("countries",countries)

    data = dict()

    for c in countries:

        country_flag = get_country_flag(c)
        graphs = list()

        pie = "pie/"+ c.country_name + ".png"
        count = TotalCasesData.objects.filter(country=c).count()
        if count > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_CASES)
        #else: graphs.append(GraphFile.NOT_ENOUGH_DATA_IMAGE)

        count = TotalCriticalData.objects.filter(country=c).count()
        if count > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_CRITICAL)
        #else: graphs.append(GraphFile.NOT_ENOUGH_DATA_IMAGE)

        count = TotalDeathsData.objects.filter(country=c).count()
        if count > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_DEATHS)
        #else: graphs.append(GraphFile.NOT_ENOUGH_DATA_IMAGE)

        count = TotalRecoveredData.objects.filter(country=c).count()
        if count > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_RECOVERED)
        #else: graphs.append(GraphFile.NOT_ENOUGH_DATA_IMAGE)

        data[str(c.country_name)] = (country_flag,pie,graphs)

    return render(request,"main_app/index.html", context={"data":data})

def home(request):
    prefix = GraphFile.stable_path
    countries = Country.objects.all().order_by('-continent_id')
    print("countries",countries)

    data = dict()

    for c in countries:

        country_flag = get_country_flag(c)
        graphs = list()

        pie = "pie/"+ c.country_name + ".png"
        count = TotalCasesData.objects.filter(country=c).count()
        if count > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_CASES)
        #else: graphs.append(GraphFile.NOT_ENOUGH_DATA_IMAGE)

        count = TotalCriticalData.objects.filter(country=c).count()
        if count > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_CRITICAL)
        #else: graphs.append(GraphFile.NOT_ENOUGH_DATA_IMAGE)

        count = TotalDeathsData.objects.filter(country=c).count()
        if count > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_DEATHS)
        #else: graphs.append(GraphFile.NOT_ENOUGH_DATA_IMAGE)

        count = TotalRecoveredData.objects.filter(country=c).count()
        if count > GraphFile.MINIMUM_NUMBER_OF_DATAPOINTS:
            graphs.append(prefix + c.country_name+GraphFile.TOTAL_RECOVERED)
        #else: graphs.append(GraphFile.NOT_ENOUGH_DATA_IMAGE)

        data[str(c.country_name)] = (country_flag,pie,graphs)

    return render(request,"main_app/index.html", context={"data":data})



