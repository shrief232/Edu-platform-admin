from django.urls import path
from .views import(
    FinalQuestionListView, FinalUserAnswerCreateView, FinalQuizResultView, GenerateCertificateView
)

urlpatterns = [
    path('questions/<int:course_id>', FinalQuestionListView.as_view(), name='final-question-list'),
    path('submit-answer/', FinalUserAnswerCreateView.as_view(), name='final-submit-answer'),
    path('result/', FinalQuizResultView.as_view(), name='final-quiz-result'),
    path('generate-certificate/', GenerateCertificateView.as_view(), name='generate-certificate'),
]