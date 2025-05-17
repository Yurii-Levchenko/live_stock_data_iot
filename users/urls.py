from django.urls import path
from .views import custom_logout_view, profile_view, edit_profile, register_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/', profile_view, name='user-profile'),  # Updated to point to the new profile view
    path('profile/edit/', edit_profile, name='edit-profile'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('logout/', custom_logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# next_page='/login/'