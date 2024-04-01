from django.urls import path
from .views import SignupAPIView,UserUpdateAPIView,LoginView,RefreshTokenView,JobView,CurrentUserView, AllUsersView, NewsLetterSubscriberView
urlpatterns = [
#   path("get-details",UserDetailAPI.as_view()),
  path('register',SignupAPIView.as_view()),
  path('login',LoginView.as_view()),
  path('refresh',RefreshTokenView.as_view()),
  path('job',JobView.as_view()),
  path('current_user',CurrentUserView.as_view()),
  path('users',AllUsersView.as_view()),
  path('update_user/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
 path('news_letter', NewsLetterSubscriberView.as_view()),

]