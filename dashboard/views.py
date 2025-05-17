from django.views.generic import TemplateView


class FavoritesTemplateView(TemplateView):
    template_name = "dashboard/favorites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        context['stocks'] = profile.favorite_tickers.all()
        context['user'] = self.request.user
        return context

