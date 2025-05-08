from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from rest_framework import routers

urlpatterns = [
    path('products/', views.ProductListCreateApiView.as_view()),
    path('products/filter', views.FilterViewSet.as_view()),
    path('products/<int:pk>/', views.ProductDetailSet.as_view()),
    # path('orders/', views.OrderViewSet.as_view()),
    # path('user-order/', views.UserOrderListApiView.as_view()),
    # path('products/info', views.ProductInfoViewSet.as_view()),
    # path('silk/', include('silk.urls', namespace='silk')),
]

router = DefaultRouter()
router.register('orders', views.OrderViewSet)
urlpatterns += router.urls