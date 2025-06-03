from django.contrib import admin
from .models import UserCourseProfile, CompletedLesson


@admin.register(UserCourseProfile)
class UserCourseProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'progress_percentage', 'user_rating')
    search_fields = ('user__username', 'course__title')
    list_filter = ('is_course_completed', 'user_rating')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'course')

    def get_progress(self, obj):
        total = obj.course.lessons.count()
        completed = obj.completed_lessons.count()
        return f"{completed}/{total}" if total > 0 else "0/0"
    get_progress.short_description = 'Progress'


admin.site.register(CompletedLesson)    