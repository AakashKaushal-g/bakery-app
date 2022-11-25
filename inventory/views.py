from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    print(request)
    return HttpResponse("Welcome to inventory App")