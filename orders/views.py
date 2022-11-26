from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

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
        return HttpResponse("Invalid API Call.Please refer to documentation for correct usage of APIs")


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
        return HttpResponse("Invalid API Call.Please refer to documentation for correct usage of APIs")


def placeOrder(request):
    return HttpResponse("API under development")
