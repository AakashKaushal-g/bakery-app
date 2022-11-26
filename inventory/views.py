from django.http import HttpResponse
import json
from . models import Inventory
from django.views.decorators.csrf import csrf_exempt

### Inventory APIs
API_ERR_MSG = "Invalid API Call.Please refer to documentation for correct usage of APIs"
AUTH_ERR_MSG = "Access Denied"

def home(request):
    return HttpResponse("Welcome to inventory App")

@csrf_exempt
def getInventory(request):
    if protocolCheck(request,'GET'):
        if adminCheck(request):
            inventory = Inventory.objects.all()
            ingredients = []
            if inventory:
                for item in inventory:
                    itemData = {}
                    itemData['name'] = item.ingredientName
                    itemData['quantity'] = item.quantity
                    itemData['last_updated'] = item.dateModified
                    ingredients.append(itemData)
            response = {
                'ingredient' : ingredients
            }

            return HttpResponse(json.dumps(response))

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
    try:
        prevItem = Inventory.objects.get(ingredientName=itemName)
        if prevItem:
            prevItem.quantity = prevItem.quantity+quantity
            prevItem.save()

        else:
            inventoryItem = Inventory(
                ingredientName = itemName,
                quantity = quantity
            )
            inventoryItem.save()
            
        return None
    except Exception as e:
        print(str(e))
        return itemName