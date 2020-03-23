from django.shortcuts import render
from .api.api import *
from django.http import HttpResponse

# Create your views here.

def run_db_scripts(request):
    populate_db()
    return HttpResponse("Done")