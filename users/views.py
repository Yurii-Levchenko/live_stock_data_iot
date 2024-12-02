from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import login


def custom_logout_view(request):
    logout(request)
    return redirect('/users/login/')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'users/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'users/register.html')

        # Create the user and profile
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user)  # Automatically create a profile for the user
        login(request, user)  # Log the user in automatically after registration
        messages.success(request, 'Registration successful!')
        return redirect('dashboard:home')  # Redirect to the dashboard or homepage

    return render(request, 'users/register.html')


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # Handle email update
        email = request.POST.get('email')
        if email:
            request.user.email = email
            request.user.save()
            messages.success(request, "Your email has been updated successfully!")
            return redirect('user-profile')

    return render(request, 'users/profile.html', {'user': request.user, 'profile': profile})


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'user': request.user, 'profile': profile})

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            request.user.email = email
            request.user.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('user-profile')  # Redirect to profile page after update

    return render(request, 'users/edit_profile.html', {'user': request.user, 'profile': profile})

# class LoginView(APIView):
#     def post(self, request):
#         from django.contrib.auth import authenticate
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             tokens = generate_tokens(user)
#             return Response({'tokens': tokens}, status=200)
#         return Response({'error': 'Invalid credentials'}, status=400)



# class UserProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         profile = Profile.objects.get(user=request.user)
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data)

# class RegisterUserView(APIView):
#     def post(self, request):
#         serializer = RegisterUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             tokens = generate_tokens(user)
#             return Response({'tokens': tokens}, status=201)
#         return Response(serializer.errors, status=400)






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