from django.db import models
from users.models import CustomUser
from django.utils import timezone
from final.models import Certificate, FinalQuizResult
from quizzes.models import QuizResult
from django.db.models import Avg 
import profiles.models 

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('ar', 'Arabic')], default='en')

    def __str__(self):
        return self.title
    
    def is_completed_by_user(self, user):
        """تحقق إذا كان المستخدم قد شاهد جميع دروس الكورس"""
        total_lessons = self.lessons.count()
        if total_lessons == 0:
            return False  
        watched_count = WatchedLesson.objects.filter(
            user=user, 
            lesson__course=self
        ).count()
        return watched_count >= total_lessons

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class WatchedLesson(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)
    watched_duration = models.PositiveIntegerField(default=0)  


    class Meta:
        unique_together = ('user', 'lesson')

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey('profiles.UserCourseProfile', on_delete=models.CASCADE, related_name='reviews', null=True)

    class Meta:
        unique_together = ('course', 'user')

    def __str__(self):
        return f"{self.user.first_name} - {self.course.title} - {self.rating}"

class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class LessonQuestion(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='student_questions')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lesson_questions')
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question by {self.user.username} on {self.lesson.title}"

class LessonAnswer(models.Model):
    question = models.OneToOneField(LessonQuestion, on_delete=models.CASCADE, related_name='answer')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lesson_answers')  
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user.username} to Question ID {self.question.id}"



