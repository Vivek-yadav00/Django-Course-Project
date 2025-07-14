from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views
from .views import stock_list,create_stock,get_stock,delete,update

urlpatterns = [
    path('', stock_list, name="stock-list"),                       # GET all stocks
    path('create/', create_stock, name="stock-create"),            # POST create stock
    path('<int:id>/', get_stock, name="stock-detail"),             # GET single stock
    path('delete/<int:id>/', delete, name="stock-delete"),         # DELETE stock
    path('update/<int:id>/', update, name="stock-update"),         # PUT update stock
]
