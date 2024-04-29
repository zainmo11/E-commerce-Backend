from django.urls import path

from .views import OrderDetailView, ViewPerformOrdersView

urlpatterns = [
    path("order/", ViewPerformOrdersView.as_view()),
    path("order/<int:pk>/", OrderDetailView.as_view()),
]
