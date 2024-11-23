from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Stock, StockPrice
from .serializers import StockSerializer, StockPriceSerializer

class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    @action(detail=True, methods=['get'])
    def prices(self, request, pk=None):
        stock = self.get_object()
        prices = StockPrice.objects.filter(stock=stock)
        serializer = StockPriceSerializer(prices, many=True)
        return Response(serializer.data)
