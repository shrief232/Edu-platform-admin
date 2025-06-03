from django.urls import path
from .views import (
    CourseListCreateView, CourseDetailView, CourseRatingStatsView,
    LessonCreateView, CourseLessonsListView, LessonDetailView,
    MarkLessonWatchedView, CourseReviewListCreateView,
    EnrollInCourseView, EnrollmentCoursesListView,LessonQuestionListCreateView, LessonAnswerCreateView
    
)

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list-create'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('<int:course_id>/lessons/', CourseLessonsListView.as_view(), name='course-lessons'),
    path('lessons/<int:lesson_id>/mark-watched/', MarkLessonWatchedView.as_view(), name='mark-lesson-watched'),
    path('<int:course_id>/reviews/', CourseReviewListCreateView.as_view(), name='course-reviews'),
    path('<int:course_id>/stats/', CourseRatingStatsView.as_view(), name='course-rating-stats'),
    path('<int:course_id>/enroll/', EnrollInCourseView.as_view(), name='course-enroll'),
    path('my-enrollments/', EnrollmentCoursesListView.as_view(), name='my-enrollments'),
    path('lessons/<int:lesson_id>/questions/', LessonQuestionListCreateView.as_view(), name='lesson-questions'),
    path('questions/answer/', LessonAnswerCreateView.as_view(), name='answer-question'),
      
]
