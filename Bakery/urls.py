from django.contrib import admin
from django.urls import include, path
from orders import views as orderViews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),
    path('login', orderViews.login, name='login'),
    path('order', orderViews.placeOrder, name='placeOrder'),
    
]
