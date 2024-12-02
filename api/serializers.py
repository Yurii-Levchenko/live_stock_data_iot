from django.urls import reverse
from rest_framework import serializers
from dashboard.models import Stock, StockPrice
from users.models import Profile
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter


class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'url', 'ticker', 'name', 'sector']
        extra_kwargs = {
            'url': {'view_name': 'stocks-detail', 'lookup_field': 'pk'}
        }
        
    def get_link(self, obj):
        request = self.context.get('request')
        return reverse('stocks-detail', args=[obj.pk], request=request)


class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = '__all__'

# User and Profile Serializers
class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'favorite_tickers']
