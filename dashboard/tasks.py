from celery import shared_task
from django.core.mail import send_mail
from dashboard.models import StockPrice, Stock
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

from django.core.cache import cache
import json
from datetime import datetime, timedelta
from django.conf import settings
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail




@shared_task
def send_weekly_summary():
    users = User.objects.all()
    one_week_ago = timezone.now() - timedelta(weeks=1)

    for user in users:
        # Skip users without a profile
        if not hasattr(user, 'profile'):
            continue
        favorites = user.profile.favorite_tickers.all()
        weekly_summary = []

        for stock in favorites:
            key = f"stock:prices:{stock.ticker}"
            prices = cache.client.get_client().lrange(key, 0, -1)
            week_prices = []
            for p in prices:
                data = json.loads(p)
                ts = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
                if ts >= one_week_ago:
                    week_prices.append(data['price'])
            if week_prices:
                highest = max(week_prices)
                lowest = min(week_prices)
                change = ((highest - lowest) / lowest) * 100 if lowest else 0
                weekly_summary.append({
                    'ticker': stock.ticker,
                    'highest_price': highest,
                    'lowest_price': lowest,
                    'price_change': change
                })
            else:
                weekly_summary.append({
                    'ticker': stock.ticker,
                    'highest_price': 'N/A',
                    'lowest_price': 'N/A',
                    'price_change': 0
                })

        summary_text = "\n".join([
            f"{item['ticker']} - High: {item['highest_price']} | Low: {item['lowest_price']} | Change: {item['price_change']:.2f}%"
            for item in weekly_summary
        ])

        # Only send if there is a summary
        if summary_text.strip():
            try:
                send_mail(
                    'Your Weekly Stock Summary',
                    summary_text,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                # send_mail('Test', 
                #           'Test body', 
                #           'lev4enkoyl@gmail.com', 
                #           [user.email])
                print(f"Sent to {user.email}")
            except Exception as e:
                print(f"Error sending to {user.email}: {e}")

    return "Weekly summaries sent!"






# @shared_task
# def send_weekly_summary():
#     # Get the users with favorite tickers
#     users = User.objects.all()  # You can filter only users who have favorites, if necessary

#     for user in users:
#         favorites = user.favorites.all()  # Assuming user has a many-to-many relationship with favorites
#         weekly_summary = []

#         for ticker in favorites:
#             stock = Stock.objects.get(ticker=ticker)

#             # Calculate highest and lowest prices over the past week
#             one_week_ago = timezone.now() - timedelta(weeks=1)
#             prices = StockPrice.objects.filter(stock=stock, recorded_at__gte=one_week_ago)
            
#             highest_price = prices.order_by('-price').first()  # Get the highest price
#             lowest_price = prices.order_by('price').first()   # Get the lowest price
            
#             weekly_summary.append({
#                 'ticker': stock.ticker,
#                 'highest_price': highest_price.price if highest_price else 'N/A',
#                 'lowest_price': lowest_price.price if lowest_price else 'N/A',
#                 'price_change': ((highest_price.price - lowest_price.price) / lowest_price.price) * 100 if highest_price and lowest_price else 0
#             })

#         # Send email with the summary
#         summary_text = "\n".join([f"{item['ticker']} - High: {item['highest_price']} | Low: {item['lowest_price']} | Change: {item['price_change']:.2f}%" for item in weekly_summary])
        
#         send_mail(
#             'Your Weekly Stock Summary',
#             summary_text,
#             'levchenko_yurii@knu.ua',  # Change this to a valid sender email
#             [user.email],
#             fail_silently=False,
#         )
        
#     return "Weekly summaries sent!"