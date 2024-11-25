from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from dashboard.views import StockViewSet, StockHistoryView, UserFavoriteStocksView, AllStocksView

urlpatterns = [
    path("stocks/", StockViewSet.as_view({"get": "list"}), name="api-stocks"),
    path("stocks/<str:ticker>/", StockViewSet.as_view({"get": "retrieve"}), name="api-stock-detail"),
    path("stocks/<str:ticker>/history/", StockHistoryView.as_view(), name="api-stock-history"),
    path("favorites/", UserFavoriteStocksView.as_view(), name="api-favorites"),
    path("all-stocks/", AllStocksView.as_view(), name="api-all-stocks"),
    
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
