from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class CustomDefaultRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        class APIRootView(APIView):
            def get(self, request, *args, **kwargs):
                return Response({
                    'stocks': reverse('stocks-list', request=request),
                    'stock-detail': 'Available at /api/stocks/{id}/',
                    'stock-history': 'Available at /api/stocks/{id}/history/',
                    'favorites': reverse('favorites-list', request=request),
                    'profile': reverse('profile-list', request=request),
                    'register': reverse('register-list', request=request),  # Register a user
                    'token-obtain': reverse('token_obtain_pair', request=request),  # Obtain JWT token
                    'token-refresh': reverse('token_refresh', request=request),  # Refresh JWT token
                })
        return APIRootView.as_view()
