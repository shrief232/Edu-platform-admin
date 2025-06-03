from rest_framework import serializers
from .models import Question, Choice, UserAnswer, QuizResult

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'lesson', 'text', 'choices']

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }  

    def validate(self, data):
        question = data['question']
        selected_choice = data['selected_choice']
        if selected_choice.question != question:
            raise serializers.ValidationError("هذا الخيار لا ينتمي للسؤال المحدد")
        return data


class QuizResultSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = QuizResult
        fields = ['id', 'lesson', 'lesson_title', 'score', 'total_questions', 'percentage', 'created_at']

    def get_percentage(self, obj):
        if obj.total_questions == 0:
            return 0
        return round((obj.score / obj.total_questions) * 100, 2)
