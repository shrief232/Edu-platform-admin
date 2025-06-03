from django.urls import path
from .views import QuestionListView, UserAnswerCreateView, QuizResultsView, CourseQuizResultView, SubmitQuizView

urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('submit-answer/', UserAnswerCreateView.as_view(), name='submit-answer'),
    path('results/', QuizResultsView.as_view(), name='quiz-results'),
    path('course-result/', CourseQuizResultView.as_view(), name='course-quiz-result'),
    path('submit-quiz/', SubmitQuizView.as_view(), name='submit-quiz'),
]
