from django.http import HttpResponse
from django.shortcuts import render

### Inventory APIs

def home(request):
    print(request)
    return HttpResponse("Welcome to inventory App")

### Bakery Items APIs
def itemsHome(request):
    print(request)
    print(request.session['member_id'])
    return HttpResponse("Welcome to inventory Items part")
