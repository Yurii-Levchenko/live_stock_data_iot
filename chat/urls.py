from django.urls import path
from .views import home, chat_view, new_chat

app_name = "chat"

urlpatterns = [
    path('', home, name='home'),
    path('new/', new_chat, name='new_chat'),
    path('<str:id>/', chat_view, name='chat'),
]