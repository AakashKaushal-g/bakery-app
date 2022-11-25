from django.urls import include, path
from . import views

urlpatterns = [
   path('', views.home, name='inventoryHome'),
   path('itemHome', views.itemsHome, name='itemHome')
]