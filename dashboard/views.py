from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Stock, StockPrice
from .serializers import StockSerializer, StockPriceSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView


class StockViewSet(ViewSet):
    def list(self, request):
        """List all stocks"""
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

    def retrieve(self, request, ticker=None):
        """Get details of a specific stock"""
        try:
            stock = Stock.objects.get(ticker=ticker)
            serializer = StockSerializer(stock)
            return Response(serializer.data)
        except Stock.DoesNotExist:
            return Response({'error': 'Stock not found'}, status=404)


class StockHistoryView(APIView):
    def get(self, request, ticker):
        """Get historical prices for a stock"""
        try:
            stock = Stock.objects.get(ticker=ticker)
            prices = StockPrice.objects.filter(stock=stock).order_by('-timestamp')
            serializer = StockPriceSerializer(prices, many=True)
            return Response(serializer.data)
        except Stock.DoesNotExist:
            return Response({'error': 'Stock not found'}, status=404)


# class StockViewSet(ModelViewSet):
#     queryset = Stock.objects.all()
#     serializer_class = StockSerializer

#     @action(detail=True, methods=['get'])
#     def prices(self, request, pk=None):
#         stock = self.get_object()
#         prices = StockPrice.objects.filter(stock=stock)
#         serializer = StockPriceSerializer(prices, many=True)
#         return Response(serializer.data)

