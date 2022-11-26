from django.urls import include, path
from . import views

urlpatterns = [
   path('', views.home, name='inventoryHome'),
   path('getInventory', views.getInventory, name='getInventorye'),
   path('addInventory', views.addInventory, name='addInventorye'),
   path('itemHome', views.itemsHome, name='itemHome')
   
]