import datetime
from rest_framework import serializers
from courses.serializers import CourseSerializer, LessonSerializer, ReviewSerializer
from .models import UserCourseProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Enrollment, WatchedLesson, CompletedLesson
from final.models import Review
from users.models import CustomUser

@receiver(post_save, sender=Enrollment)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserCourseProfile.objects.create(
            user=instance.user,
            course=instance.course,
            enrollment=instance
        )

@receiver(post_save, sender=WatchedLesson)
def update_completed_lessons(sender, instance, **kwargs):
    profile = UserCourseProfile.objects.get(
        user=instance.user, 
        course=instance.lesson.course
    )
    lesson = instance.lesson
    
    # Check if watched duration >= 90% of lesson duration
    if instance.watched_duration >= (lesson.duration_minutes * 60 * 0.9):
        CompletedLesson.objects.get_or_create(
            profile=profile,
            lesson=lesson,
            defaults={'time_spent': instance.watched_duration}
        )
    profile.update_progress()

@receiver(post_save, sender=Review)
def link_review_to_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserCourseProfile.objects.get(
            user=instance.user,
            course=instance.course
        )
        instance.profile = profile
        instance.save()
        profile.user_rating = instance.rating
        profile.save()