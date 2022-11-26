from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json
from inventory.models import BakeryItem,Inventory
# Create your views here.
API_ERR_MSG = "Invalid API Call.Please refer to documentation for correct usage of APIs"

####################
### Login/Logut
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

def placeOrder(request):
    pass
    ## Reserve Inventory

    ## Create Order ID

    ## Create Order
