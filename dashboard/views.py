from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dashboard.models import Stock


class FavoritesTemplateView(TemplateView):
    template_name = "dashboard/favorites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        context['stocks'] = profile.favorite_tickers.all()
        context['user'] = self.request.user
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class RemoveFavoriteView(TemplateView):
    def post(self, request, *args, **kwargs):
        ticker = request.POST.get('ticker')
        try:
            stock = Stock.objects.get(ticker=ticker)
            profile = request.user.profile
            profile.favorite_tickers.remove(stock)
            return JsonResponse({'success': True, 'message': f'{ticker} removed from favorites'})
        except Stock.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Stock not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

