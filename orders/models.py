from django.db import models
import uuid
# Create your models here.
class Order(models.Model):
    orderID = models.CharField(max_length=32)
    itemName = models.CharField(max_length=200)
    quantity = models.FloatField(default=0)
    sellingPrice = models.FloatField(default=0)
    totalAmount = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    username = models.CharField(max_length=50)

    def createOrderID() :
        return str(uuid.uuid4().hex)