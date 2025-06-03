import uuid
from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError  
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse, FileResponse
from profiles.models import UserCourseProfile, CompletedLesson


from .models import Course, Lesson, WatchedLesson, Review, Enrollment, LessonQuestion
from .serializers import CourseSerializer, LessonSerializer, ReviewSerializer, EnrollmentSerializer, LessonQuestionSerializer, LessonAnswerSerializer

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]

class CourseLessonsListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        user = self.request.user
        if not Enrollment.objects.filter(user=user, course_id=course_id).exists():
            raise ValidationError("You must enroll in this course to view lessons.")
        return Lesson.objects.filter(course_id=course_id)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class MarkLessonWatchedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        duration = request.data.get("watched_duration", 0)
        user = request.user

        watched, created = WatchedLesson.objects.get_or_create(user=user, lesson=lesson)

        if not created and duration > watched.watched_duration:
            watched.watched_duration = duration
            watched.save()
        elif created:
            watched.watched_duration = duration
            watched.save()

        # Update UserCourseProfile
        profile, _ = UserCourseProfile.objects.get_or_create(user=user, course=lesson.course)
        CompletedLesson.objects.get_or_create(profile=profile, lesson=lesson, defaults={'time_spent': duration})
        profile.current_lesson = lesson
        profile.update_progress()

        return Response({'message': 'تم التعليم كمشاهد'}, status=status.HTTP_200_OK)


class CourseReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Review.objects.filter(course_id=course_id).order_by('-created_at')

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        if Review.objects.filter(user=self.request.user, course_id=course_id).exists():
            raise ValidationError("You've already reviewed this course")
        serializer.save(user=self.request.user, course_id=course_id)

class CourseRatingStatsView(APIView):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        avg_rating = course.reviews.aggregate(avg=Avg('rating'))['avg'] or 0.0
        total_reviews = course.reviews.count()

        return Response({
            'course_id': course_id,
            'average_rating': round(avg_rating, 1),
            'total_reviews': total_reviews
        }, status=status.HTTP_200_OK)

class EnrollInCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = Course.objects.filter(id=course_id).first()
        if not course:
            return Response({'detail': 'Course not found'}, status=404)

        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return Response({'detail': 'You are already enrolled in this course'}, status=400)

        enrollment = Enrollment.objects.create(user=request.user, course=course)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=201)

class EnrollmentCoursesListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(enrollment__user=self.request.user)


class LessonQuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonQuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_id']
        if self.request.user.is_staff:  
            return LessonQuestion.objects.filter(lesson_id=lesson_id, user=self.request.user ).order_by('-created_at')
        return LessonQuestion.objects.filter(lesson_id=lesson_id, user=self.request.user).order_by('-created_at')


    def perform_create(self, serializer):
        lesson_id = self.kwargs['lesson_id']
        lesson = get_object_or_404(Lesson, id=lesson_id) 
        serializer.save(user=self.request.user, lesson=lesson)

class LessonAnswerCreateView(generics.CreateAPIView):
    serializer_class = LessonAnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        question = serializer.validated_data['question']
        if hasattr(question, 'answer'):
            raise ValidationError("This question already has an answer.")
        serializer.save(user=self.request.user)


