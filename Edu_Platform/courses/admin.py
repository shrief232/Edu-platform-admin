from django.contrib import admin
from .models import Course, Lesson, WatchedLesson, Review, Enrollment, LessonQuestion, LessonAnswer

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'instructor', 'language', 'created_at')
    search_fields = ('title', 'description', 'instructor__username')
    list_filter = ('language', 'created_at')
   

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'course', 'order', 'duration_minutes')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)
    

@admin.register(WatchedLesson)
class WatchedLessonAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'watched_at', 'watched_duration')
    search_fields = ('user__username', 'lesson__title')
    list_filter = ('watched_at',)
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    search_fields = ('user__username', 'course__title', 'comment')
    list_filter = ('rating', 'created_at')
    

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    search_fields = ('user__username', 'course__title')
    list_filter = ('enrolled_at',)
    

@admin.register(LessonQuestion)
class LessonQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'created_at')
    search_fields = ('user__username', 'lesson__title', 'question_text')
    list_filter = ('created_at',)
    

@admin.register(LessonAnswer)
class LessonAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created_at')
    search_fields = ('user__username', 'answer_text', 'question__question_text')
    list_filter = ('created_at',)
    
