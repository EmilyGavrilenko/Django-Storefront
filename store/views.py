from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

@api_view()
def product_list(request):
    product_set = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(product_set, many=True, context={'request': request})
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view()
def collection_detail(request, id):
    collection = get_object_or_404(Collection, pk=id)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)
