from django.urls import include, path
from . import views

urlpatterns = [
   path('', views.home, name='inventoryHome'),
   path('getIngredients', views.getIngredients, name='getIngredients'),
   path('addIngredients', views.addIngredients, name='addIngredients'),
   path('addBakeryItem', views.addBakeryItem, name='addBakeryItem'),
   path('getBakeryItem', views.getBakeryItem, name='getBakeryItem'),
   path('itemHome', views.itemsHome, name='itemHome')
   
]