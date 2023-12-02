
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [

    path('pay/<str:orderid>',webprint),
    path('ccavRequestHandler/',ccavRequestHandler),
    path('ccavResponseHandler/',ccavResponseHandler)



]
