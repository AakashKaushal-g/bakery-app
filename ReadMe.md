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
###### Payload element
1. ** username (string) ** : This is the username which will used to login to the app later. There needs to be a username which is unique for each user.
2. ** password (string) ** : The pass string which is used to authentocate the user.
3. ** firstName (string) ** : First name of the user.
4. ** lastName (string) ** : Last name of the user
5. ** mail (string) ** : The email address of the user.

