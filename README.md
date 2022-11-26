# Bakery-app Documentation

The API URL , mentions the details the endpoint from where API can be accesses

To access the APIs for bakery, the user needs to register with the bakery using **register** API.
After the registration is successful, the user needs to login to the app in order to access the APIs using **login** API.

## Gerenal APIs
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
- (string) Registration Successful for 'userName'

After Registeration User can, Login to the Application to use the APIs.

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
- (string) Login Successful
 
After Registeration User can, Login to the Application to use the APIs

### Logout (GET)
**URL : /logout**
##### Sample Payload :
```
None
```
This API can be used to logout from the App and closing the user session

###### Success Response 
- (string) User 'userName' logged out sucessfully

========================================================

## Admin APIs

To access these APIs, the user needs to login withan admin/superuser account.
Accessing thes APIs without a admi/superuser account would return a response 'Access Denied'

### getIngredients (GET)
**URL : /inventory/getIngredients**
##### Sample Payload :
```
None
```
This API is used to get the ingredients available in bakery.
###### Payload elements
None

###### Success Response 
- (list) A list of All ingredients with name and quantity available

### getBakeryItems (GET)
**URL : /inventory/getBakeryItems**
##### Sample Payload :
```
None
```
This API is used to get the items available in bakery.
###### Payload elements
None

###### Success Response 
- (list) A list of All Bakery Items with the details like, prices, ingredients, discount etc.


### addIngredients (POST)
**URL : /inventory/addIngredients**
##### Sample Payload :
```
{
    "ingredients": [
        {
            "name" : "Flour",
            "quantity" : 5
        },
        {
            "name" : "Milk",
            "quantity" : 10
        }
    ]
}
```
This API is used to add ingredients in bakery inventory.
###### Payload elements
**ingredients** (list) : This is a list of Ingredients which can be updated in the inventory. Each element of the list is JSON data having keys mentioned below
**name** (string) : Name of the ingredient
**quantity** (int) : Quantity of the ingredients in units

###### Success Response 
- (string) (if ingredient is added successfully ) Ingredients added succesfully for : eggs,milk 
- (string) (if ingredient is not added successfully ) Failed to add Ingredients : eggs,milk

The API serve both purposes of insert and increment. So if the Item is not existing in the availabel records, it create and entry for the ingredient otherwise, if the entry for the same ingredient already exists, then the existing quantity is incremented by the quantity recieved in the payload


### addBakeryItem (POST)
**URL : /inventory/addBakeryItem**
##### Sample Payload :
```
{
    "name" : "Bread",
    "costPrice" : 25,
    "sellingPrice" : 40,
    "discount" : 1.25,
    "ingredients": [
        {
            "name" : "Flour",
            "quantity" : 2
        },
        {
            "name" : "Milk",
            "quantity" : 1
        }
    ]
}
```
This API is used to add items in bakery inventory.
###### Payload elements
**name** (string) : Name of the Bakery Item.
**costPrice** (float) : Cost of the Bakery item to Bakery.
**sellingPrice** (float) : Selling amount of the item.
**discount** (float) (_optional_) : Discount available of bakery item. If not provided , it will be defaulted to 0
**ingredients** (list) : This is a list fo Ingredients which is required to prepare the item. Each element of the list is JSON data having keys mentioned below
**name** (string) : Name of the ingredient to be used
**quantity** (int) : Quantity of the ingredients required (in units)

###### Success Response 
- (string) (When Bakery item is added) Added Bakery Item : nameOfItem 
- (string) (When Bakery item is added) Updated Bakery Item : nameOfItem

The API serve both purposes of insert and update. So if the Item is not existing in the available records, it create and entry for the bakery otherwise, if the entry for the same bakery already exists, then the existing details are updated by the recentrly received details in payload.

### updateDiscount (PATCH)
**URL : /inventory/updateDiscount**
##### Sample Payload :
```
{
    "name" : "Bread",
    "discount" : 12
}
```
This API is used to update discount value for items in bakery inventory.
###### Payload elements
**name** (string) : Name of the Bakery Item.
**discount** (float) : Discount to updated for bakery item.

###### Success Response 
- (string) Discount Value updated for item 'nameOfItem'


### discardIngredients (DELETE)
**URL : /inventory/discardIngredients**
##### Sample Payload :
```
{
    "name" :
    [
        "eggs","flour"
    ]
    
}
```
This API is used to add items in bakery inventory.
###### Payload elements
**name** (list) : List of Names of the Bakery Items to be deleted

###### Success Response 
- (string) (if element is not present) Ingredients not found : eggs,flour 
- (string) (if element is present) Ingredients deleted : eggs,flour 


========================================================

## Customer APIs
These are the APIs which are supposed to be used by customers ot interact with Bakery, so check the items available and place orders.

### checkItems (GET)
**URL : /checkItems**
##### Sample Payload :
```
None
```
This API is used to get the items available in bakery for selling.
###### Payload elements
None

###### Success Response 
- (list) A list of All Bakery Items with the details like, prices, discount etc.

### TopSellingItems (GET)
**URL : /getTopSellingItems**
##### Sample Payload :
```
None
```
This API is used to get the most popular items available in bakery.
###### Payload elements
None

###### Success Response 
- (list) A list of 5 most sold Bakery Items with the details in order of populatrity.

### order (POST)
**URL : /order**
##### Sample Payload :
```
{
    "order":
    [
        {
            "name" : "Bread",
            "quantity" : 2
        }
    ]
}
```
This API is used to order items from bakery inventory.
###### Payload elements
**order** (list) : This is a list of Items which are being ordered, Each element of the list is JSON data having keys mentioned below
**name** (string) : Name of the Item 
**quantity** (int) : Quantity of the items required

###### Success Response 
- (string) (if sufficient ingredients are available for to complete order ) Successfully placed the order. Order id : ' 32-character hex ID '
- (string) (if sufficient ingredients are available to serve the order ) Unable to Place order. Not enough stock

When a order is placed, there are 3 operations which are performed :
- Resource Reservation : Accoruding to the qunatity of Bakery item request and the recipie of the item, resources are resevred in order to cater thte order at hand
- Order ID generation : Once resources are reserved, the Order ID is generated. This is an unique a 32-Character hexadecimal string
- Order Generation :  Obce the ableve two processes are done, the order is placed and the confirmation of the order placement is responsed back to the user.



### getOrderHistory (GET)
**URL : /getOrderHistory**
##### Sample Payload :
```
None
```
This API is used to get the order history of the logged in user
###### Payload elements
None

###### Success Response 
- (list) A list of most recent 10 order form the logged in user

====================================
====================================

For any issues/concerns please connecte with me over email : aakashkaushal75@gmail.com

