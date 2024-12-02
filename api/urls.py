from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import StockViewSet, UserFavoriteStocksViewSet, UserProfileViewSet, RegisterUserViewSet
from .routers import CustomDefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


# Create a router and register the viewsets
router = CustomDefaultRouter()
router.register(r'stocks', StockViewSet, basename='stocks')
router.register(r'favorites', UserFavoriteStocksViewSet, basename='favorites')
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'register', RegisterUserViewSet, basename='register')

schema_view = get_schema_view(
    openapi.Info(
        title="Stock API",
        default_version='v1',
        description="API for managing stocks and user profiles",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@stocks.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),  # Include the router-generated URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
