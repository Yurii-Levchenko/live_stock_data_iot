from django.urls import path
from .views import StockViewSet, StockHistoryView, UserFavoriteStocksView, AllStocksView
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard/dashboard.html'), name='home'),
    path('stocks/', StockViewSet.as_view({'get': 'list'}), name='api-stocks'),
    path('stocks/<str:ticker>/', StockViewSet.as_view({'get': 'retrieve'}), name='api-stock-detail'),
    path('stocks/<str:ticker>/history/', StockHistoryView.as_view(), name='api-stock-history'),
    path('favorites/', UserFavoriteStocksView.as_view(), name='favorites'),
    path('all-stocks/', AllStocksView.as_view(), name='all-stocks'),
]
