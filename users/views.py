from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer, RegisterUserSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'users/register.html')  # Render the registration form
    
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
            return redirect('login')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)