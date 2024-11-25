from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Stock, StockPrice
from .serializers import StockSerializer, StockPriceSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class StockViewSet(ViewSet):
    # permission_classes = [IsAuthenticated]
    def list(self, request):
        stocks = Stock.objects.all()
        data = []
        for stock in stocks:
            # Get the latest price for each stock
            latest_price = StockPrice.objects.filter(stock=stock).order_by('-timestamp').first()
            data.append({
                'ticker': stock.ticker,
                'price': float(latest_price.price) if latest_price else None,
                'timestamp': latest_price.timestamp.strftime('%Y-%m-%d %H:%M:%S') if latest_price else 'N/A',
            })
        return Response(data)
        # serializer = StockSerializer(stocks, many=True)
        # return Response(serializer.data)

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



class UserFavoriteStocksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        favorite_stocks = profile.favorite_tickers.all()
        stocks_data = [{"ticker": stock.ticker, "name": stock.name} for stock in favorite_stocks]
        return Response(stocks_data)

    def post(self, request):
        ticker = request.data.get("ticker")
        try:
            stock = Stock.objects.get(ticker=ticker)
            profile = request.user.profile
            profile.favorite_tickers.add(stock)
            return Response({"message": f"{ticker} added to favorites."}, status=status.HTTP_201_CREATED)
        except Stock.DoesNotExist:
            return Response({"error": "Stock not found."}, status=status.HTTP_404_NOT_FOUND)


# class UserFavoriteStocksView(APIView):
#     def get(self, request):
#         profile = request.user.profile
#         favorite_stocks = profile.favorite_tickers.all()
#         serializer = StockSerializer(favorite_stocks, many=True)
#         return Response(serializer.data)

class AllStocksView(APIView):
    def get(self, request):
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

# class StockViewSet(ModelViewSet):
#     queryset = Stock.objects.all()
#     serializer_class = StockSerializer

#     @action(detail=True, methods=['get'])
#     def prices(self, request, pk=None):
#         stock = self.get_object()
#         prices = StockPrice.objects.filter(stock=stock)
#         serializer = StockPriceSerializer(prices, many=True)
#         return Response(serializer.data)

