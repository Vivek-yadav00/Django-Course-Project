from django.shortcuts import render
from rest_framework.response import Response
from .models import Stock
from .serials import StockSerializers
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache 
from rest_framework import status

# Create your views here.

@api_view(['GET'])
def stock_list(request):
    ordering=request.GET.get('ordering','')
    page=request.GET.get('page','1')
    key=f"stock_list_{page}_{ordering}"
    cached_response=cache.get(key)

    if cached_response:
        return Response(cached_response)


    if ordering:
        stocks=Stock.objects.all().order_by(ordering)
    else:
        stocks=Stock.objects.all()
        
    paginator= PageNumberPagination()
    paginator.page_size=10
    result_page=paginator.paginate_queryset(stocks,request)
    serializer= StockSerializers(result_page,many=True)
    paginated_data=paginator.get_paginated_response(serializer.data).data

    cache.set(key,paginated_data,timeout=300)
    return Response(paginated_data)


@api_view(['POST'])
def create_stock(request):
    #json to object
    serializer=StockSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_stock(request,id):
    try:
        stock=Stock.objects.get(pk=id)
    except:
        return Response({'error':'Stock not found'},status=status.HTTP_404_NOT_FOUND)
    
    serializer=StockSerializers(stock)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete(request,id):
    try:
        stock=Stock.objects.get(pk=id)
    except:
        return Response({'error':'Stock not found'},status=status.HTTP_404_NOT_FOUND)
    
    stock.delete()
    return Response(status=status.HTTP_200_OK)



@api_view(['PUT','PATCH'])
def update(request,id):
    try:
        stock=Stock.objects.get(pk=id)
    except:
        return Response({'error':'Stock not found'},status=status.HTTP_404_NOT_FOUND)
    
    serializer=StockSerializers(stock,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)