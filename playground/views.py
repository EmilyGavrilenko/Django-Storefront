from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Avg, Max, Min, Sum
from django.db import transaction, connection
from store.models import Product, Customer, Collection, Order, OrderItem, CartItem, Cart
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem

def say_hello(request):
    """
    # Get object by primary key (throws exception if not found)
    product = Product.objects.get(pk=1) # Returns 1 product
    # Get object by primary key (returns None if not found)
    product = Product.objects.filter(pk=1).first() # Returns 1 product or None
    # Get object by primary key (returns true/false for it it's found)
    product_exists = Product.objects.filter(pk=1).exists() # Returns true or false
    # Returns a query to get all products. Lazily executes after the variable is used
    products = Product.objects.all() # Returns a query to get products
    # Returns a query to get all products where price is 20
    products = Product.objects.filter(unit_price=20) # Returns list of products
    # Returns a query to get all products where price > 20
    products = Product.objects.filter(unit_price__gt=20) # Returns list of products
    # Returns a query to get all products where 20 < price < 30
    products = Product.objects.filter(unit_price__range=(20, 22)) # Returns list of products
    # Returns a query to get all products where the collection is in the list
    products = Product.objects.filter(collection__id__range=(3,4)) # Returns list of products
    # Returns a query to get all products where the title contains the name (case insensitive)
    products = Product.objects.filter(title__icontains='bread') # Returns list of products
    # Returns a query to get all products where the update year is 2021
    products = Product.objects.filter(last_update__year=2021) # Returns list of products
    # Returns a query to get all products where the update year is 2021
    products = Product.objects.filter(last_update__year=2021) # Returns list of products
    """
    
    """ Practice problems """
    """
    # Customers with .com accounts
    customer_set = Customer.objects.filter(email__endswith='.com') 
    # Collections that don’t have a featured product
    customer_set = Collection.objects.filter(featured_product__isnull=True) 
    # Products with low inventory (less than 10)
    customer_set = Product.objects.filter(inventory__lt=10) 
    # Orders placed by customer with id = 1
    customer_set = Order.objects.filter(customer_id=1) 
    # Order items for products in collection 3
    customer_set = OrderItem.objects.filter(product__collection_id=3) 
    """
    ## Inventory < 10 and price < 20
    # result = Product.objects.filter(inventory__lt=10, unit_price__lt=20) 
    ## result = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20) 
    # Inventory < 10 OR price < 20
    # result = Product.objects.filter(Q(inventory__lt=10) | ~Q(unit_price__lt=20))
    ## Products: Inventory = price
    # result = Product.objects.filter(inventory=F('unit_price'))

    # # Products: alphabetically by price and title desc
    # result = Product.objects.order_by('unit_price', '-title')
    # # Products: get the cheapest product
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.order_by('unit_price').first()
    # product = Product.objects.earliest('unit_price')

    # # Return first 5 products
    # result = Product.objects.all()[:5]
    # # Specify fields you want to query
    # result = Product.objects.values('id', 'title', 'collection__title')
    # # Select products that have been ordered and sort them by title
    # result = OrderItem.objects.values('product_id').distinct().order_by('product__title').values('product_id', 'product__title').order_by('product_id')

    # # Select products that have been ordered and sort them by title
    # # selected_related (1 match)
    # result = Product.objects.select_related('collection').all()
    # # prefetch_related (* matches)
    # result = Product.objects.prefetch_related('promotions').all()
    # # Fetch all products and their promotions and collections
    # result = Product.objects.prefetch_related('promotions').select_related('collection').all()

    
    ## Get the last 5 orders with their customer and items (incl product)
    # result = Order.objects.select_related('customer').values('customer__first_name')[:1]
    # result = Order.objects.select_related('customer').prefetch_related('orderitems').values()[:1]#'customer__first_name', 'customer__last_name', 'product__title')[:1]
    # result = Order.objects.select_related('customer').order_by('-placed_at')[:5]#'customer__first_name', 'customer__last_name', 'product__title')[:1]
    # result = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]#'customer__first_name', 'customer__last_name', 'product__title')[:1]

    """ Aggregation practice """
    # # How many orders do we have?
    # result = Order.objects.aggregate(order_count=Count('id'))
    ## How many units of product 1 have we sold?
    # result = OrderItem.objects.filter(product_id=1).aggregate(units_sold=Sum('quantity'))
    # result = Order.objects.prefetch_related('orderitem_set__product').values('product__title', 'product__price')[:3]#.aggregate(order_count=Count('id'))
    # # How many orders has customer 1 placed?
    # result = Order.objects.filter(customer_id=1).aggregate(customer_order_count=Count('id'))
    # # What is the min, max and average price of the products in collection 3?
    # result = Product.objects.filter(collection_id=3).aggregate(minPrice=Min('unit_price'), maxPrice=Max('unit_price'), avgPrice=Avg('unit_price'))
    
    """ Annotations practice """
    # # Give each customer a new field is_new  = True(1)
    # result = Customer.objects.annotate(is_new=Value(True), new_id=F('id'))
    # # Calculate full name of customer
    # result = Customer.objects.annotate(full_name=Func(F("first_name"), Value(' '), F("first_name"), function='CONCAT'))
    # result = Customer.objects.annotate(full_name=Concat("first_name", Value(' '), "first_name"))
    # # Calculate # of orders per customers
    # result = Customer.objects.annotate(orders_count=Count("order"))

    """ Expression Wrapper """
    # discount_func = ExpressionWrapper(F("unit_price") * 0.8, output_field=DecimalField(max_digits=6, decimal_places=2)) 
    # result = Product.objects.annotate(discounted_price=discount_func)

    """ Annotation Practice """
    # # Customers with their last order ID
    # result = Customer.objects.annotate(last_order_id=Max('order__id'))
    # # Collections and count of their products 
    # result = Collection.objects.annotate(product_count=Count('product'))
    # # Customers with more than 5 orders 
    # result = Customer.objects.annotate(order_count=Count('order')).filter(order_count__gt=5)
    # # Customers and the total amount they’ve spent 
    # result = Customer.objects.annotate(total_spent=Sum(F('order__orderitem__unit_price') * F('order__orderitem__quantity')))
    # # Top 5 best-selling products and their total sales 
    # result = Product.objects.annotate(total_sales=Sum(F('orderitem__unit_price') * F('orderitem__quantity'))).order_by('-total_sales')[:5]

    """ Generic Relations """
    # # Content type ID for product
    # result = TaggedItem.objects.get_tags_for(Product, 1)

    """ Queryset Cache """
    # result = Product.objects.all()
    # list(result)
    # print(result)

    """ Creating Objects """
    # # Option 1
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product.objects.get(pk=1)
    # collection.save()
    # # Option 2
    # collection = Collection.objects.create(title='Video Games', featured_product_id=1)


    """ Update Objects """
    # # Option 1
    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()
    # # Option 2
    # collection = Collection.objects.filter(pk=11).update(featured_product=None)


    """ Delete Objects """
    # # Option 1
    # collection = Collection(pk=11)
    # collection.delete()
    # # Option 2
    # Collection.objects.filter(id__gt=8).delete()

    """ Creating, Updating, and Removing Objects """
    # # Create a shopping cart with an item
    # cart = Cart.objects.create()
    # item = CartItem.objects.create(cart_id=cart.id, product_id=9, quantity=2)
    ## Update the quantity of an item in a shopping cart 
    # item = CartItem.objects.filter(pk=1).update(quantity=3)
    # # Remove a shopping cart with its items 
    # Cart.objects.filter(pk=1).delete()

    """ Transactions """
    # with transaction.atomic():
    #     order = Order.objects.create(customer_id=1)
    #     print(order)
    #     item = OrderItem.objects.create(order_id=order.id, product_id=-1, quantity=1, unit_price=10)
    #     print(item)

    """ Raw SQL """
    # # Option 1
    # result = Product.objects.raw('SELECT * FROM store_product')
    # # Option 2
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT * from store_product')
    #     cursor.callproc('get_customers', [1,2,'a'])
    
    result = {}
    return render(request, 'hello.html', {'name': 'Mosh', 'products': [], 'result': result})
