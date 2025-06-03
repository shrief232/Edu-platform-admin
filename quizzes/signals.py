from django.db.models.signals import post_save
from django.dispatch import receiver
from quizzes.models import QuizResult
from profiles.models import UserCourseProfile

@receiver(post_save, sender=QuizResult)
def update_user_quiz_score(sender, instance, **kwargs):
    try:
        profile = UserCourseProfile.objects.get(user=instance.user, course=instance.lesson.course)
        profile.calculate_scores()
    except UserCourseProfile.DoesNotExist:
        pass
