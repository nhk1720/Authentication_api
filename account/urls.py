
from django.urls import path,include
from account.views import UserRegistationview,UserLoginView,UserProfileView,ChangePasswordView,UserPasswordResetView,SendPasswordEmailView

urlpatterns = [
    path("register/",UserRegistationview.as_view()),
    path("login/",UserLoginView.as_view()),
    path("profile/",UserProfileView.as_view()),
    path("reset/",ChangePasswordView.as_view()),
    path('send-reset-password-email/',SendPasswordEmailView.as_view()),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view())
]