from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from pprint import pprint

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
pprint(router.urls)

# URLConf
# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls))
]