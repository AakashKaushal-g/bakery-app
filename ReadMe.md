# Bakery-app Documentation

The API URL , mentions the details the endpoint from where API can be accesses

To access the APIs for bakery, the user needs to register with the bakery using **register** API.
After the registration is successful, the user needs to login to the app in order to access the APIs using **login** API.

### Register (POST)
**URL : /register**
##### Sample Payload :
```
{
    "username" : "newuser",
    "password" : "pass,123",
    "firstName": "New",
    "lastName": "user",
    "mail": "newuser@bakery.com"
}
```
This API is used whena new user has to register to the Bakery app.

###### Payload elements
1. **username** (string) : This is the username which will used to login to the app later. There needs to be a username which is unique for each user.
2. **password** (string)  : The pass string which is used to authentocate the user.
3. **firstName** (string) : First name of the user.
4. **lastName** (string) : Last name of the user
5. **mail** (string) : The email address of the user.

###### Success Response 
Registration Successful for '<userName>'

After Registeration User can, Login to the Application to use the APIs.

========================================================

### Login (POST)
**URL : /login**
##### Sample Payload :
```
{
    "username" : "newuser",
    "password" : "pass,123",
}
```
This API can be used to login to the App, enabling the user to use othe APIs offered.
###### Payload elements
1. **username** (string): This is the username which will used to login to the app later. There needs to be a username which is unique for each user.
2. **password** (string)  : The pass string which is used to authentocate the user.

###### Success Response 
Login Successful
 
After Registeration User can, Login to the Application to use the APIs

### Logout (GET)
**URL : /logout**
##### Sample Payload :
```
None
```

This API can be used to logout from the App and closing the user session

###### Success Response 
User '<userName>' logged out sucessfully

========================================================
## Admin APIs

To access these APIs, the user needs to login withan admin/superuser account.
Accessing thes APIs without a admi/superuser account would return a response 'Access Denied'

### Login (POST)
**URL : /login**
##### Sample Payload :
```
{
    "username" : "newuser",
    "password" : "pass,123",
}
```
This API can be used to login to the App, enablung the user to use othe APIs offered.
###### Payload elements
1. **username** (string): This is the username which will used to login to the app later. There needs to be a username which is unique for each user.
2. **password** (string)  : The pass string which is used to authentocate the user.
