from django.urls import path
from django.views.generic import TemplateView
from dashboard.views import FavoritesTemplateView, RemoveFavoriteView

urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard/dashboard.html'), name='home'),
    path("favorites/", FavoritesTemplateView.as_view(), name="favorites"),
    path("favorites/remove/", RemoveFavoriteView.as_view(), name="remove_favorite"),
]
