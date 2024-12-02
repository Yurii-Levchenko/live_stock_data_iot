from django.urls import path
from django.views.generic import TemplateView
from dashboard.views import FavoritesTemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard/dashboard.html'), name='home'),
    path("favorites/", FavoritesTemplateView.as_view(), name="favorites"),
]
