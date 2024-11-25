from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer, RegisterUserSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = generate_tokens(user)
            return Response({'tokens': tokens}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            tokens = generate_tokens(user)
            return Response({'tokens': tokens}, status=200)
        return Response({'error': 'Invalid credentials'}, status=400)
    
# class RegisterUserView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         return render(request, 'users/register.html')  # Render the registration form
    
#     def post(self, request):
#         serializer = RegisterUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
#             return redirect('login')
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)