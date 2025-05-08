from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerailizer, OrderCreateSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Product, Order
from django.db.models import Max
from rest_framework import generics, filters, viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser, AllowAny
from api.filters import ProductFilter, InStockFilter, OrderFilter


# Create your views here.

class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilter,
    ]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_size_query_param = 'page_size'
    pagination_class_query_param = 'pagination_class'
    # pagination_class.
    search_fields = ["=name", "description"]
    ordering_fields = ["name", "price", "stock"]
    # filterset_fields = ['name', 'price']
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ProductDetailSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_url_kwarg = 'product_id'
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class FilterViewSet(generics.ListAPIView):
    queryset = Product.objects.filter(price__lt=20)
    serializer_class = ProductSerializer

class OrderViewSet(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ProductInfoViewSet(generics.ListAPIView):
    def get(self, request):
        products = Product.objects.all()
        data = {
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        }
        serializer = ProductInfoSerailizer(data)
        return Response(serializer.data)

# class UserOrderListApiView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         user = self.request.user
#         qs = super().get_queryset()
#         return qs.filter(user=user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product,pk=pk)
#     serailizer = ProductSerializer(product)
#     return Response(serailizer.data)

# @api_view(['GET'])
# def order_detail(request):
#     order = Order.objects.all()
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def view_info(request):
#     products = Product.objects.all()
#     serailizer = ProductInfoSerailizer({
#         'products': products,
#         'count': len(products),
#         'max_price': products.aggregate(max_price=Max('price'))['max_price']
#     })
#     return Response(serailizer.data)