from django.http import HttpResponse
import json
from . models import Inventory,BakeryItem
from django.views.decorators.csrf import csrf_exempt

API_ERR_MSG = "Invalid API Call.Please refer to documentation for correct usage of APIs"
AUTH_ERR_MSG = "Access Denied"


#############################
### Inventory APIs
#############################

def home(request):
    return HttpResponse("Welcome to inventory App")

def getIngredients(request):
    if protocolCheck(request,'GET'):
        if adminCheck(request):
            inventory = Inventory.objects.all()
            ingredients = []
            if inventory:
                for item in inventory:
                    itemData = {}
                    itemData['name'] = item.ingredientName
                    itemData['quantity'] = item.quantity
                    itemData['last_updated'] = str(item.dateModified.strftime("%d-%m-%Y %H:%M:%S"))
                    ingredients.append(itemData)
            response = {
                'ingredient' : ingredients
            }
            return HttpResponse(json.dumps(response),content_type="application/json")

        else:
            return HttpResponse(AUTH_ERR_MSG)
    else:
        return HttpResponse(API_ERR_MSG)

@csrf_exempt
def addIngredients(request):
    if protocolCheck(request,'POST'):
        if adminCheck(request):
            ingredientList = json.loads(request.body)
            insertResponse = {
                'success': [],'failure': []
            }

            for ingredient in ingredientList['ingredients']:
                flag = addDetails(ingredient['name'].lower(),ingredient['quantity']) 
                if flag:
                    insertResponse['success'].append(ingredient['name'])
                else:
                    insertResponse['failure'].append(ingredient['name'])
            message = ''
            if insertResponse['success']:
                message+="Ingredients added succesfully for : {} .".format(','.join(insertResponse['success']))
            if insertResponse['failure']:
                message+="Failed to add Ingredients : {}.".format(','.join(insertResponse['failure']))

            return HttpResponse(message)


        else:
            return HttpResponse(AUTH_ERR_MSG)
    else:
        return HttpResponse(API_ERR_MSG)

#############################
### Bakery Items APIs
#############################

@csrf_exempt
def addBakeryItem(request):
    if protocolCheck(request,'POST'):
        if adminCheck(request):
            try:
                itemData = json.loads(request.body)
                
                itemName = itemData['name']
                ingredientList = [str(ingredient['name']) for ingredient in itemData['ingredients']]
                quantityList = [str(ingredient['quantity']) for ingredient in itemData['ingredients']]
                if 'discount' in itemData.keys():
                    discount = itemData['discount']
                else:
                    discount=0

                previousData = BakeryItem.objects.filter(itemName=itemName)
                if previousData:
                    previousData = previousData[0]
                    
                    previousData.costPrice = itemData['costPrice']
                    previousData.sellingPrice = itemData['sellingPrice']
                    previousData.ingredientList = ",".join(ingredientList)
                    previousData.quantityList = ",".join(quantityList)
                    previousData.discount = discount
                    previousData.save()
                    return HttpResponse("Updated Bakery Item : {}".format(itemName))

                else:
                    item = BakeryItem(
                        itemName = itemName,
                        costPrice = itemData['costPrice'],
                        sellingPrice = itemData['sellingPrice'],
                        ingredientList = ",".join(ingredientList),
                        quantityList = ",".join(quantityList),
                        discount = discount
                    )
                    item.save()
                    return HttpResponse("Added Bakery Item : {}".format(itemName))

            except Exception as e:
                print(str(e))

        else:
            return HttpResponse(AUTH_ERR_MSG)
    else:
        return HttpResponse(API_ERR_MSG)

def getBakeryItems(request):
    if protocolCheck(request,'GET'):
        if adminCheck(request):
            itemData = BakeryItem.objects.all()
            items = []
            for item in itemData :
                obj = {}
                ingredientList = item.ingredientList.split(',')
                quantityList = item.quantityList.split(',')
                obj['name'] = item.itemName
                obj['costPrice'] = item.costPrice
                obj['sellingPrice'] = item.sellingPrice
                obj['discount'] = item.discount
                obj['ingredients'] = []
                for i in range(len(ingredientList)):
                    temp = {}
                    temp['name'] = ingredientList[i]
                    temp['quantity'] = quantityList[i]
                    obj['ingredients'].append(temp)

                items.append(obj)
            response = {
                "items" : items
            }
            return HttpResponse(json.dumps(response),content_type="application/json")
        else:
            return HttpResponse(AUTH_ERR_MSG)
    else:
        return HttpResponse(API_ERR_MSG)

@csrf_exempt
def updateDiscount(request):
    if protocolCheck(request,'POST'):
        if adminCheck(request):
            try:
                itemData = json.loads(request.body)
                discount = itemData['discount']
                if type(discount) != float and type(discount) != int :
                    return HttpResponse("The Discount value entered is not numberical. terminating Operation")
                checkItem = BakeryItem.objects.filter(itemName = itemData['name'])
                if checkItem:
                    checkItem = checkItem[0]
                    checkItem.discount = discount
                    checkItem.save()
                    return HttpResponse("Discount Value updated for item '{}'".format(itemData['name']))
                else:
                    return HttpResponse("No Bakery item '{}' Exists. Please add an item to updated dicsount value for it.")
            except Exception as e :
                return HttpResponse("Error occured. {}".str(e))
        else:
            return HttpResponse(AUTH_ERR_MSG)
    else:
        return HttpResponse(API_ERR_MSG)

@csrf_exempt
def reserveIngredients(request):
    if protocolCheck(request,'POST'):
        if adminCheck(request):
            return HttpResponse("Under development")

        else:
            return HttpResponse(AUTH_ERR_MSG)
    else:
        return HttpResponse(API_ERR_MSG)

#############################
## Utility functions:
#############################

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
        print(itemName,quantity)
        previousItem = Inventory.objects.filter(ingredientName=itemName)
        
        if previousItem:
            previousItem = previousItem[0]
            previousItem.quantity = previousItem.quantity+quantity
            previousItem.save()

        else:
            inventoryItem = Inventory(
                ingredientName = itemName,
                quantity = quantity
            )
            inventoryItem.save()
            
        return True
    except Exception as e:
        print(str(e))
        return False