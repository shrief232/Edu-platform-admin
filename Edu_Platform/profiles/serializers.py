import datetime
from rest_framework import serializers
from courses.serializers import CourseSerializer, LessonSerializer, ReviewSerializer
from .models import UserCourseProfile
from courses.models import Review

class UserCourseProfileSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    completed_lessons = LessonSerializer(many=True, read_only=True)
    user_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = UserCourseProfile
        fields = [
            'course',
            'enrollment_date',
            'current_lesson',
            'is_course_completed',
            'completion_date',
            'quiz_score',
            'final_exam_score',
            'certificate',
            'last_activity',
            'total_time_spent',
            'user_rating',
            'completed_lessons',
            'reviews',
            'progress_percentage',
        ]

    def get_user_rating(self, obj):
        review = Review.objects.filter(user=obj.user, course=obj.course).first()
        return review.rating if review else None   