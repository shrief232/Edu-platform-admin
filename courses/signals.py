from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment, Review
from profiles.models import UserCourseProfile

@receiver(post_save, sender=Enrollment)
def create_user_course_profile(sender, instance, created, **kwargs):
    if created:
        UserCourseProfile.objects.get_or_create(
            user=instance.user,
            course=instance.course,
            defaults={'enrollment': instance}
        )

@receiver(post_save, sender=Review)
def update_user_rating_in_profile(sender, instance, **kwargs):
    try:
        profile = UserCourseProfile.objects.get(user=instance.user, course=instance.course)
        profile.user_rating = instance
        profile.save()
    except UserCourseProfile.DoesNotExist:
        pass  # لو مفيش Profile مش هنكريت واحد هنا