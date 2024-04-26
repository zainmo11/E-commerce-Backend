from django.urls import path

from .views import AuthenticateUserView, DummyView, RegisterUserView

urlpatterns = [
    path("login/", AuthenticateUserView.as_view()),
    path("auth-test/", DummyView.as_view()),
    path("register/", RegisterUserView.as_view()),
]
