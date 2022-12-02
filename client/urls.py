from django.urls import path
from django.conf.urls import url,include
from client.views import AllOrders,NewOrder
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('orders/',AllOrders, name='orders'),
    path('neworder/',NewOrder, name='neworder'),
    ]