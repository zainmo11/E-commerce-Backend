from django.urls import path

from .views import AuthenticateUserView, RegisterCustomerView, RegisterSellerView

urlpatterns = [
    path("login/", AuthenticateUserView.as_view()),
    path("register/", RegisterCustomerView.as_view()),
    path("register/seller/", RegisterSellerView.as_view()),
]
