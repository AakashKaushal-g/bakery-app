from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json,os,sys
from django.db.models import Sum
from inventory.models import BakeryItem,Inventory,reserveInventory
from .models import Order
# Create your views here.
API_ERR_MSG = "Invalid API Call.Please refer to documentation for correct usage of APIs"

####################
### User Management
####################

@csrf_exempt
def login(request):
    if request.method =='POST':
        try:
            inputData = json.loads(request.body)
            password = inputData['password']
            user = inputData['username']
        except Exception as e:
            print(e)
            return HttpResponse("Invalid Inputs recived. Please refer documentation fo correct usage of APIs")
        try:
            auth = authenticate(username=user,password=password)
            if auth :
                userData = User.objects.filter(username=user)
                if userData:
                    userData = userData[0]
                
                request.session['username'] = user
                request.session['isAdmin'] = bool(userData.is_superuser)
                return HttpResponse("Login Successful")

            else:
                return HttpResponse("Invalid Credentials.Please user correct credentials to login")
        except Exception as e:
            return HttpResponse("Error occured while logging in user. Exceptions => {}".format(str(e)))

    else :
        return HttpResponse(API_ERR_MSG)

def logout(request):
    if request.method =='GET':
        try:
            username = request.session['username']
            
            del request.session['username']
            del request.session['isAdmin']
            return HttpResponse("User '{}' logged out sucessfully".format(username))

        except Exception as e:
            print(e)
            return HttpResponse("No Active Session are present to log out")
        
    else :
        return HttpResponse(API_ERR_MSG)

####################
### Ordering
####################

def checkItems(request):
    if request.method == "GET":
        try:
            itemData = BakeryItem.objects.all()
            items =[]
            if itemData:
                for item in itemData:
                    obj = {}
                    obj['name'] = item.itemName
                    obj['price (Rs.)'] = item.sellingPrice
                    obj['dicount (%)'] = item.discount
                    items.append(obj)
            response = {
                'Available Items' : items
            }
            return HttpResponse(json.dumps(response),content_type="application/json")
        except Exception as e :
            return HttpResponse("Error Occured : {}".format(str(e)))
    else:
        return HttpResponse(API_ERR_MSG)

@csrf_exempt
def placeOrder(request):
    if request.method == "POST" :
        ## Reserve Inventory
        if request.session['username'] : 
            user=  request.session['username']
            orderPrices = []
            try:
                orderData = json.loads(request.body)
                orders = orderData['order']
                for order in orders:
                    itemName = order['name']
                    quantity = order['quantity']

                    itemData = BakeryItem.objects.filter(itemName = itemName)
                    if itemData :
                        itemData = itemData[0]

                        tempData = {}
                        tempData['name'] = itemData.itemName
                        tempData['quantity'] = quantity
                        tempData['discount'] = itemData.discount
                        tempData['price'] = itemData.sellingPrice
                        orderPrices.append(tempData)
                        reserveFlag,successItem = reserveResouces(itemData,quantity)
                        if reserveFlag :
                            try:
                                for row in successItem:
                                    obj = reserveInventory(
                                        ingredientName = row['name'],
                                        quantity = row['qty']
                                    )
                                    obj.save()
                            except Exception as e :
                                print(str(e))
                                return HttpResponse("Unable to Place order. Resources not reserved")
                        else:
                            return HttpResponse("Unable to Place order. Not enough stock")
                    else:
                        return HttpResponse("Unable to Place order. Not enough stock")        
            except Exception as e :
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return HttpResponse("Error Occured. {}".format(str(e)))

            ## Create Order ID
            orderId = Order.createOrderID()

            ## Create Order
            if orderId and orderPrices :
                for entry in orderPrices :
                    discountedPrice = (1 - (entry['discount']/100))*entry['price']
                    totalPrice = entry['quantity']*discountedPrice

                    try:
                        obj = Order(
                            orderID = orderId,
                            itemName = entry['name'],
                            quantity = entry['quantity'],
                            sellingPrice = entry['price'],
                            totalAmount = totalPrice,
                            discount = entry['discount'],
                            username = user
                        )
                        obj.save()
                        return HttpResponse("Successfully placed the order. Order id : ' {} '".format(orderId))    
                        
                    except Exception as e :
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        return HttpResponse("Unable to Place order. Trouble adding order. '{}'".format(str(e)))    
            else:
                return HttpResponse("Unable to Place order. OrderID not generated")
        else:
            return HttpResponse("No user is logged in. Access Denied")
    else:
        return HttpResponse(API_ERR_MSG)

def reserveResouces(itemData,quantity):
    try:
        failureItem=[];successItem = []
        IngredientList = itemData.ingredientList.split(',')
        quantityList = itemData.quantityList.split(',')
        
        for i in range(len(IngredientList)):
            name = IngredientList[i].lower()
            qty = float(quantityList[i])*quantity

            existingData = reserveInventory.objects.filter(ingredientName = name.lower())
            existingCount = 0
            if existingData :
                existingCount = list(reserveInventory.objects.filter(ingredientName = name.lower()).aggregate(Sum('quantity')).values())[0]
            totalCount = Inventory.objects.filter(ingredientName = name)
            if totalCount:
                totalCount = totalCount[0].quantity
                if (totalCount - existingCount) > 1:
                    successItem.append({
                        'name' : name,
                        "qty" : qty
                    })
                else:
                    print("Not Enough Ingredients")
                    failureItem.append({
                        'name' : name,
                        "qty" : qty
                    })
                    break
            else:
                print('item not defined in inventory')
                failureItem.append({
                        'name' : name,
                        "qty" : qty
                    })
                break
        
        if failureItem:
            return False,[]
        else:
            return True,successItem
    except Exception as e :
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

        print("Error reserving the Resouces")
        return str(e)

def getOrderHistory(request):
    if request.method == "GET":
        if request.session['username']:
            user = request.session['username']
            userOrders = Order.objects.filter(username = user).order_by('-createdAt')
            orderData = {}
            for order in userOrders :
                orderID = order.orderID
                print
                if orderID not in orderData.keys() and len(orderData.keys()) < 11 :
                    orderData[orderID] = []

                    tempDict = {}
                    tempDict['itemName'] = order.itemName
                    tempDict['itemQuantity'] = order.quantity
                    tempDict['totalAmount'] = order.totalAmount
                    tempDict['createAt'] = str(order.createdAt.strftime("%d-%m-%Y %H:%M:%S"))

                    orderData[orderID].append(tempDict)
            
            response = {
                user : orderData
            }
            print(response)
            return HttpResponse(json.dumps(response),content_type="application/json")
        else:
            return HttpResponse("No user is logged in. Access Denied")


    else:
        return HttpResponse(API_ERR_MSG)

####################
### Misc
####################

def topSellingItems(request):
    if request.method == "GET":
        itemData = Order.objects.all()
        itemList = {}
        for item in itemData :
            itemDetails = {}
            itemName = item.itemName

            if itemName not in itemList.keys():
                itemList[itemName] = 0
            
            itemList[itemName]+=item.quantity
        
        sortedList = {k: v for k, v in sorted(itemList.items(), key=lambda item: item[1],reverse=True)}
        popularItems = [key.strip('\r\n') for key in sortedList.keys()]
        if len(popularItems) > 5:
            popularItems= popularItems[:5]
        
        response = {
            "Popular Items " : popularItems
        }
        return HttpResponse(json.dumps(response),content_type="application/json")
            
    else:
        return HttpResponse(API_ERR_MSG)