from django.contrib import admin
from .models import FinalQuestion, FinalChoice, FinalUserAnswer, FinalQuizResult, Certificate
# Register your models here.

admin.site.register(FinalQuestion)
admin.site.register(FinalChoice)
admin.site.register(FinalUserAnswer)
admin.site.register(FinalQuizResult)
admin.site.register(Certificate)