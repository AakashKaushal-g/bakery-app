from django.db import models

class Inventory(models.Model):
    ingredientName = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    dateModified = models.DateTimeField(auto_now=True)

# class reserveInventory(models.model) :
#     ingredientName = models.CharField(max_length=200)
#     quantity = models.IntegerField(default=0)
#     dateModified = models.DateTimeField(auto_now=True)

class BakeryItem(models.Model):
    itemName = models.CharField(max_length=200)
    costPrice = models.FloatField()(default=0)
    sellingPrice = models.FloatField()(default=0)
    discount = models.FloatField()(default=0)
    ingredientList = models.CharField(max_length=1000)
    quantityList = models.CharField(max_length=1000)

