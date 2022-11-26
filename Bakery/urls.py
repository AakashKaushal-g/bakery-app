from django.contrib import admin
from django.urls import include, path
from orders import views as orderViews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),
    path('login', orderViews.login, name='login'),
    path('logout', orderViews.logout, name='logout'),
    path('checkItems', orderViews.checkItems, name='checkItems'),
    path('order', orderViews.placeOrder, name='placeOrder'),
    path('orderHistory', orderViews.getOrderHistory, name='orderHistory'),
    
]
