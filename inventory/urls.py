from django.urls import include, path
from . import views

urlpatterns = [
   path('', views.home, name='inventoryHome'),
   path('getIngredients', views.getIngredients, name='getIngredients'),
   path('addIngredients', views.addIngredients, name='addIngredients'),
   path('addBakeryItem', views.addBakeryItem, name='addBakeryItem'),
   path('getBakeryItems', views.getBakeryItems, name='getBakeryItems'),
   path('updateDiscount', views.updateDiscount, name='updateDiscount'),
   
]