from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']
    # при необходимости добавьте параметры фильтрации


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filterset_fields = ['products']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     product_id = self.request.query_params.get('product')
    #     if product_id:
    #         queryset = queryset.filter(positions__product_id=product_id)
    #
    #     return queryset
