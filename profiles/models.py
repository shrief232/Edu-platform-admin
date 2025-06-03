from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import CustomUser

class UserCourseProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='course_profiles')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='user_profiles')
    
    enrollment = models.OneToOneField('courses.Enrollment', on_delete=models.SET_NULL, null=True, blank=True)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    current_lesson = models.ForeignKey('courses.Lesson', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_users')
    completed_lessons = models.ManyToManyField('courses.Lesson', through='CompletedLesson', blank=True, related_name='completed_by_users')
    is_course_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.PositiveIntegerField(default=0)
    
    quiz_score = models.FloatField(default=0)
    final_exam_score = models.FloatField(default=0)
    certificate = models.OneToOneField('final.Certificate', on_delete=models.SET_NULL, null=True, blank=True)
    
    last_activity = models.DateTimeField(auto_now=True)
    total_time_spent = models.PositiveIntegerField(default=0)
    
    user_rating = models.ForeignKey('courses.Review', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_ratings')

    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.email} - {self.course.title}"
    
    @property
    def progress(self):
        total = self.course.lessons.count()
        completed = self.completed_lessons.count()
        return int((completed / total) * 100) if total > 0 else 0
    
    def update_progress(self):
        total_lessons = self.course.lessons.count()
        completed = self.completed_lessons.count()

        progress = int((completed / total_lessons) * 100) if total_lessons > 0 else 0
        self.progress_percentage = progress

        self.is_course_completed = (completed >= total_lessons) if total_lessons > 0 else False
        if self.is_course_completed and not self.completion_date:
            self.completion_date = timezone.now()
        self.save()
    
    def calculate_scores(self):
        from quizzes.models import QuizResult
        from final.models import FinalQuizResult

       
        lesson_results = QuizResult.objects.filter(user=self.user, lesson__course=self.course)
        avg_quiz_score = lesson_results.aggregate(models.Avg('score'))['score__avg'] or 0
        max_quiz_score = 5 

        
        self.quiz_score = round((avg_quiz_score / max_quiz_score) * 100, 2)

        
        final_result = FinalQuizResult.objects.filter(user=self.user, course=self.course).first()
        if final_result:
            max_final_score = 20  
            self.final_exam_score = round((final_result.score / max_final_score) * 100, 2)
        else:
            self.final_exam_score = 0

        self.save()


class CompletedLesson(models.Model):
    profile = models.ForeignKey(UserCourseProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    time_spent = models.PositiveIntegerField(default=0)  # In seconds
    
    class Meta:
        unique_together = ('profile', 'lesson')