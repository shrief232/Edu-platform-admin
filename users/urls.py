from django.urls import path
from .views import RegisterView, UserDetailView, CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView, ProtectedView, VerifyEmailView, CheckEmailExists

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('protected/', ProtectedView.as_view(), name='protected'), 
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'), 
    path('check-email/', CheckEmailExists.as_view(), name='check-email'),

]
