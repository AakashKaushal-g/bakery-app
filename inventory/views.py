from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

### Inventory APIs
API_ERR_MSG = "Invalid API Call.Please refer to documentation for correct usage of APIs"
AUTH_ERR_MSG = "Access Denied"

def home(request):
    return HttpResponse("Welcome to inventory App")

@csrf_exempt
def getInventory(request):
    if protocolCheck(request,'POST'):
        if adminCheck(request):
            payload = json.loads(request.body)
            return HttpResponse("Under development")

        else:
            return HttpResponse(AUTH_ERR_MSG)
    else:
        return HttpResponse(API_ERR_MSG)

@csrf_exempt
def addInventory(request):
    if protocolCheck(request,'POST'):
        if adminCheck(request):
            return HttpResponse("Under development")

        else:
            return HttpResponse(AUTH_ERR_MSG)
    else:
        return HttpResponse(API_ERR_MSG)

@csrf_exempt
def reserveInventory(request):
    if protocolCheck(request,'POST'):
        if adminCheck(request):
            return HttpResponse("Under development")

        else:
            return HttpResponse(AUTH_ERR_MSG)
    else:
        return HttpResponse(API_ERR_MSG)



### Bakery Items APIs
def itemsHome(request):
    print(request)
    print(request.session['member_id'])
    return HttpResponse("Welcome to inventory Items part")

## Utility functions:
def adminCheck(request):
    try:
        return request.session['isAdmin']
    except Exception as e:
        print(e)
        return False

def protocolCheck(request,protocol):
    try:
        if request.method == protocol.upper():
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def addDetails(itemName,quantity):
    pass