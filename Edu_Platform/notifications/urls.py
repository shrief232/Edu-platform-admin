from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/mark-read/', views.MarkNotificationAsRead.as_view(), name='mark-notification-read'),
    path('mark-all-read/', views.mark_all_read, name='mark-all-read'),
]