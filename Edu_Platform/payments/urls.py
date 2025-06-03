from django.urls import path
from .views import PaymentListView, PaymentCreateView

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('create-payment/', PaymentCreateView.as_view(), name='create-payment'),
]
