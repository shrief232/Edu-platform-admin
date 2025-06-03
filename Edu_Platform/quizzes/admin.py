from django.contrib import admin
from .models import Question, Choice, UserAnswer, QuizResult

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2  
    show_change_link = True

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'lesson')
    search_fields = ('text', 'lesson__title')
    list_filter = ('lesson',)
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text', 'question__text')
    list_filter = ('is_correct',)
    

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_choice', 'created_at')
    search_fields = ('user__username', 'question__text', 'selected_choice__text')
    list_filter = ('created_at',)
   

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'score', 'total_questions', 'created_at')
    search_fields = ('user__username', 'lesson__title')
    list_filter = ('created_at',)
    
