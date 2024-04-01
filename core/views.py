from django.shortcuts import render
from .models import User,Job,NewsLetterSubscriberModel
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer,JobSerializer,NewsLetterSubscriberSerializer
from django.contrib.auth import authenticate ,login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveAPIView,UpdateAPIView, ListAPIView,ListCreateAPIView,CreateAPIView
from django.contrib.auth.hashers import make_password

#Class based view to register user
class SignupAPIView(CreateAPIView):
    serializer_class = UserSerializer
    
    
       
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            result={
                'message': 'Login successful.',
                'access': str(refresh.access_token),
                "user":serializer.data
            }
            return Response(result)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(APIView):
   def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return Response({'access_token': access_token},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class JobView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobSerializer(data=request.data, context={"userinfo":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CurrentUserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
    
    
    
    
class AllUsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def perform_update(self, serializer):
        serializer.save()

class NewsLetterSubscriberView(ListCreateAPIView):
     queryset = NewsLetterSubscriberModel.objects.all()
     serializer_class = NewsLetterSubscriberSerializer
    #  permission_classes = [IsAuthenticated]