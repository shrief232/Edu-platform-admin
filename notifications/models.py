from django.db import models
from users.models import CustomUser


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('answer', 'إجابة على سؤال'),
        ('course_completed', 'استكمال كورس'),
        ('course_enrolled', 'التحاق بكورس'),
        ('course_reviewed', 'تقييم كورس'),
        ('lesson_completed', 'استكمال درس'),
        ('lesson_question_answered', 'إجابة على سؤال درس'),
        ('lesson_watched', 'مشاهدة درس'),
        ('new_course', 'كورس جديد'),
        ('new_lesson', 'درس جديد'),
        ('new_quiz', 'اختبار جديد'),
        ('quiz_completed', 'استكمال اختبار'),
        ('quiz_reviewed', 'تقييم اختبار'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"

    class Meta:
        ordering = ['-created_at']