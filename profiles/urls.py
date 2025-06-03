from django.urls import path
from .views import UserCourseProfileView, UserCourseProfileListView

urlpatterns = [
    path('user-course-profile/<int:course_id>/',UserCourseProfileView.as_view(),name='user-course-profile'),
    path('user-course-profile/', UserCourseProfileListView.as_view(), name='user-course-profile-list'),

]

