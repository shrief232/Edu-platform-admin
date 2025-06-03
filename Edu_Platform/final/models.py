from django.db import models
from django.conf import settings
from django.utils import timezone

class FinalQuestion(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='final_questions')
    text = models.CharField(max_length=500)
    
    def __str__(self):
        return self.text

class FinalChoice(models.Model):
    question = models.ForeignKey(FinalQuestion, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Wrong'})"

class FinalUserAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(FinalQuestion, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(FinalChoice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'question')

class FinalQuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    score = models.FloatField()
    total_questions = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey('profiles.UserCourseProfile', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user} - {self.course} - {self.score}/{self.total_questions}"

class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    certificate_id = models.CharField(max_length=100, unique=True)
    score = models.FloatField()
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"Certificate for {self.user} - {self.course}"