from django.urls import path
from django.conf.urls import url,include
from merchant.views import AllClients,AddClient,AddTyreCategory,AddTyre,EditOrder,AllOrders,UpdateOrder,OrderToUpdate,AllOrderswithoutfilter
from django.contrib.auth.views import LoginView
urlpatterns = [ 
    url(r'^clients/$', AllClients),
    url(r'^newclient/$', AddClient),
    url(r'^addtyrecategory/$', AddTyreCategory),
    url(r'^addtyre/$', AddTyre),
    path('order/<id>/', EditOrder),
    path('updateorder/<id>/', UpdateOrder),
    url(r'^ordertoupdate/$', OrderToUpdate),
    url(r'^allorders/$', AllOrderswithoutfilter),
    url(r'^orders/$', AllOrders),
    ]