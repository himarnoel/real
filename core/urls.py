from django.urls import path
from .views import SignupAPIView,LoginView,RefreshTokenView,JobView
urlpatterns = [
#   path("get-details",UserDetailAPI.as_view()),
  path('register',SignupAPIView.as_view()),
  path('login',LoginView.as_view()),
  path('refresh',RefreshTokenView.as_view()),
  path('job',JobView.as_view()),
]