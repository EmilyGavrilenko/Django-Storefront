from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem
from decimal import Decimal
from django.forms.models import model_to_dict


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)



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
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product', 'total_price']

    product = ProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self, item: CartItem):
        return item.product.unit_price * item.quantity
    
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    cart_items = CartItemSerializer(source='items', many=True)

    class Meta:
        model = Cart
        fields = ['id', 'cart_items', 'total_price']

    total_price = serializers.SerializerMethodField(method_name='calculate_total_cart_price')

    def calculate_total_cart_price(self, cart: Cart):
        item_subtotals = [item.product.unit_price * item.quantity for item in cart.items.all()]
        total = sum(item_subtotals)
        return total