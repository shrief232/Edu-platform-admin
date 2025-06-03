from rest_framework import serializers
from .models import FinalChoice, FinalQuestion, FinalUserAnswer, FinalQuizResult, Certificate



class FinalChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalChoice
        fields = ['id', 'text', 'is_correct']

class FinalQuestionSerializer(serializers.ModelSerializer):
    choices = FinalChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = FinalQuestion
        fields = ['id', 'course', 'text', 'choices']

class FinalUserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalUserAnswer
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def validate(self, data):
        question = data['question']
        selected_choice = data['selected_choice']
        if selected_choice.question != question:
            raise serializers.ValidationError("هذا الخيار لا ينتمي لهذا السؤال")
        return data

class FinalQuizResultSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = FinalQuizResult
        fields = ['id', 'course', 'course_title', 'score', 'total_questions', 'percentage', 'created_at']

    def get_percentage(self, obj):
        if obj.total_questions == 0:
            return 0
        return round((obj.score / obj.total_questions) * 100, 2)
    
class CertificateSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Certificate
        fields = ['id', 'user', 'user_name', 'course', 'course_title', 'issue_date', 'certificate_id', 'score']