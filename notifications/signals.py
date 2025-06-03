from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Enrollment, LessonAnswer    
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=LessonAnswer)
def create_answer_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.question.user,
            message=f"Your question has been answered.: {instance.question.question_text[:30]}...",
            notification_type='answer',
            url=f"/lessons/{instance.question.lesson.id}/questions/"
        )
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.question.user.id}",
            {
                "type": "send_notification",
                "message": f"Your question has been answered. {instance.question.question_text[:30]}..."
            }
        )

@receiver(post_save, sender=Enrollment)
def create_course_completion_notification(sender, instance, created, **kwargs):
    if instance.is_completed:  
        Notification.objects.create(
            user=instance.user,
            message=f"Congratulations! You have completed the course. {instance.course.title}",
            notification_type='course_completed',
            url=f"/courses/{instance.course.id}/"
        )