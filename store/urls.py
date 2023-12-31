from django.urls import path, include
from . import views
from pprint import pprint
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('collections', views.CollectionViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

# Products
router.register('products', views.ProductViewSet, basename='products')
# Products/Reviews nested router
product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
product_router.register('images', views.ProductImageViewSet, basename='product-images')

# Carts
router.register('carts', views.CartViewSet)
# Cart items nested router
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')


# URLConf
# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(carts_router.urls))
]