from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'unit_price', 'price_with_tax', 'inventory', 'collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = CollectionSerializer()

    # Hyperlink related field
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail',
    #     lookup_field='id'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)    
