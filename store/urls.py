from django.urls import path, include
from . import views
from pprint import pprint
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
pprint(router.urls)

# URLConf
# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls))
]