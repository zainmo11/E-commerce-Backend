from django.urls import path

from .views import AuthenticateUserView, RegisterSellerView, RegisterUserView

urlpatterns = [
    path("login/", AuthenticateUserView.as_view()),
    path("register/", RegisterUserView.as_view()),
    path("register/seller/", RegisterSellerView.as_view()),
]
