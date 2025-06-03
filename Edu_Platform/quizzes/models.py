from django.db import models
from django.conf import settings

class Question(models.Model):
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    
    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Wrong'})"

class UserAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'question')
    
    def __str__(self):
        return f"{self.user} - {self.question}"

class QuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE)
    score = models.FloatField()
    total_questions = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey('profiles.UserCourseProfile', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'lesson')
    
    def __str__(self):
        return f"{self.user} - {self.lesson} - {self.score}/{self.total_questions}"