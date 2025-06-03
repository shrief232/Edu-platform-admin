from rest_framework import serializers
from .models import Course, Lesson, WatchedLesson, Review, Enrollment, LessonQuestion, LessonAnswer

class LessonSerializer(serializers.ModelSerializer):
    is_watched = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_is_watched(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return WatchedLesson.objects.filter(user=user, lesson=obj).exists()

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'created_at', 'language', 'lessons', 'is_completed']
        read_only_fields = ['instructor', 'created_at']

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_completed_by_user(request.user)
        return False    

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'course', 'user', 'username', 'rating', 'first_name', 'last_name','comment', 'created_at']
        read_only_fields = ['user', 'created_at', 'course']

    def validate(self, attrs):
        user = self.context['request'].user
        course = self.context['view'].kwargs.get('course_id')
        if Review.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("You've already reviewed this course")
        return attrs

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at']
        read_only_fields = ['user', 'enrolled_at']



class LessonAnswerSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = LessonAnswer
        fields = ['id', 'question', 'user', 'user_name', 'answer_text', 'created_at']
        read_only_fields = ['user', 'created_at']

class LessonQuestionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    answer = LessonAnswerSerializer(read_only=True)

    class Meta:
        model = LessonQuestion
        fields = ['id', 'lesson', 'user', 'user_name', 'question_text', 'created_at', 'answer']
        read_only_fields = ['user', 'created_at', 'lesson']



