from django.urls import path
from .views import UserProfileView, RegisterUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('register/', RegisterUserView.as_view(), name='register'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# next_page='/login/'