from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:id>/', views.collection_detail, name='collection-detail')
]
