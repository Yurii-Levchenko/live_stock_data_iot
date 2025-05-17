from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import StockSerializer, StockPriceSerializer, ProfileSerializer, RegisterUserSerializer
from dashboard.models import Stock, StockPrice
from users.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User


# Stock and StockPrice Views

class StockViewSet(ModelViewSet):
    """
    A ModelViewSet for CRUD operations on stocks
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        stocks = Stock.objects.all()
        result = []
        for stock in stocks:
            latest_price = StockPrice.objects.filter(stock=stock).order_by('-recorded_at').first()
            result.append({
                'ticker': stock.ticker,
                'price': latest_price.price if latest_price else None,
                'latest_price_time': latest_price.recorded_at.strftime('%Y-%m-%d %H:%M:%S') if latest_price else None,
                'market_status': stock.market_status or 'N/A',
                'exchange': stock.exchange or 'N/A',
            })
        return Response(result)

    # def list(self, request):
    #     """
    #     List all available stocks.
    #     """
    #     stocks = Stock.objects.all()
    #     serializer = StockSerializer(stocks, many=True, context={'request': request})
    #     return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve details of a specific stock by its ID.
        """
        try:
            stock = Stock.objects.get(pk=pk)
            serializer = StockSerializer(stock, context={'request': request})
            return Response(serializer.data)
        except Stock.DoesNotExist:
            return Response({'error': 'Stock not found'}, status=404)

    @action(detail=True, methods=['get'], url_path='history')
    def history(self, request, pk=None):
        """
        Get historical prices for a stock.
        """
        try:
            stock = Stock.objects.get(pk=pk)
            prices = StockPrice.objects.filter(stock=stock).order_by('-timestamp')
            serializer = StockPriceSerializer(prices, many=True, context={'request': request})
            return Response(serializer.data)
        except Stock.DoesNotExist:
            return Response({'error': 'Stock not found'}, status=404)



class UserFavoriteStocksViewSet(ModelViewSet):
    """
    A ModelViewSet for managing user favorite stocks.
    """
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    serializer_class = StockSerializer

    def get_queryset(self):
        return self.request.user.profile.favorite_tickers.all()

    def list(self, request):
        """
        List favorite stocks of the authenticated user.
        """
        favorites = self.get_queryset()
        serializer = StockSerializer(favorites, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='add')
    def add_favorite(self, request):
        """
        Add a stock to the user's favorites.
        """
        ticker = request.data.get("ticker")

        print(f"Trying to add ticker: {ticker}")
        print(f"User: {request.user}")

        if not request.user.is_authenticated:
            return Response({"error": "JWT Authentication required (Token is missing)."}, status=401)
        
        try:
            stock = Stock.objects.get(ticker=ticker)
            profile = request.user.profile
            profile.favorite_tickers.add(stock)
            return Response({"message": f"{ticker} added to favorites."})
        except Stock.DoesNotExist:
            return Response({"error": "Stock not found."}, status=404)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": str(e)}, status=500)

    @action(detail=False, methods=['post'], url_path='remove')
    def remove_favorite(self, request):
        """
        Remove a stock from the user's favorites.
        """
        ticker = request.data.get("ticker")
        try:
            stock = Stock.objects.get(ticker=ticker)
            profile = request.user.profile
            profile.favorite_tickers.remove(stock)
            return Response({"message": f"{ticker} removed from favorites."})
        except Stock.DoesNotExist:
            return Response({"error": "Stock not found."}, status=404)


# User and Authentication Views

class UserProfileViewSet(ModelViewSet):
    """
    A ModelViewSet for managing user profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


# class UserProfileViewSet(ViewSet):
#     permission_classes = [IsAuthenticated]

#     def list(self, request):
#         profile = Profile.objects.get(user=request.user)
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data)



class RegisterUserViewSet(ModelViewSet):
    """
    A ViewSet for user registration.
    """
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request):
        """
        Register a new user and return tokens.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response({'tokens': tokens}, status=201)
        return Response(serializer.errors, status=400)


# class RegisterUserViewSet(ViewSet):
#     def create(self, request):
#         """Register a new user and return tokens."""
#         serializer = RegisterUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)
#             tokens = {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }
#             return Response({'tokens': tokens}, status=201)
#         return Response(serializer.errors, status=400)


def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            tokens = generate_tokens(user)
            return Response({'tokens': tokens}, status=200)
        return Response({'error': 'Invalid credentials'}, status=400)
