from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        product_set = Product.objects.select_related('collection').all()[:10]
        serializer = ProductSerializer(product_set, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

@api_view(['GET', 'PUT'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view()
def collection_detail(request, id):
    collection = get_object_or_404(Collection, pk=id)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)
