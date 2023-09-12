from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models import Count
from rest_framework.views import APIView

class ProductList(APIView):
    def get(self, request):
        product_set = Product.objects.select_related('collection').all()[:10]
        serializer = ProductSerializer(product_set, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            return Response({'error': "Product cannot be deleted cause it's associated with an order item"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        collection_set = Collection.objects.annotate(products_count=Count('product')).all()
        serializer = CollectionSerializer(collection_set, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    
@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, id):
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count('product')), 
        pk=id
    )
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.product_set.count() > 0:
            return Response({'error': "Collection cannot be deleted cause it's associated with at least 1 product"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


