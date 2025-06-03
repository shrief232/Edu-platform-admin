from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Count, Sum
from rest_framework.generics import RetrieveAPIView
from .models import Question, Choice, UserAnswer, QuizResult
from .serializers import QuestionSerializer, UserAnswerSerializer, QuizResultSerializer
from courses.models import Course, Lesson
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        lesson_id = self.request.query_params.get('lesson')
        if lesson_id:
            return Question.objects.filter(lesson_id=lesson_id)
        return Question.objects.none()
    
# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from .models import UserAnswer, Question, QuizResult
# from .serializers import UserAnswerSerializer

class UserAnswerCreateView(generics.CreateAPIView):
    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={
            'question': request.data.get('question'),
            'selected_choice': request.data.get('selected_choice')
        })
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data['question']
        user = request.user

        # التأكد من أن المستخدم لم يجب على هذا السؤال من قبل
        if UserAnswer.objects.filter(user=user, question=question).exists():
            return Response(
                {"detail": "لقد قمت بالإجابة على هذا السؤال مسبقاً"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # حفظ إجابة المستخدم
        serializer.save(user=user)

        # التحقق مما إذا أكمل المستخدم جميع أسئلة الدرس
        lesson = question.lesson
        total_questions = Question.objects.filter(lesson=lesson).count()
        user_answers_count = UserAnswer.objects.filter(user=user, question__lesson=lesson).count()

        if user_answers_count == total_questions:
            correct_answers = UserAnswer.objects.filter(
                user=user,
                question__lesson=lesson,
                selected_choice__is_correct=True
            ).count()

            # إنشاء أو تحديث نتيجة الاختبار للمستخدم
            QuizResult.objects.update_or_create(
                user=user,
                lesson=lesson,
                defaults={
                    'score': correct_answers,
                    'total_questions': total_questions
                }
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class QuizResultsView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        lesson_id = request.query_params.get('lesson')
        
        correct_answers = UserAnswer.objects.filter(
            user=request.user,
            question__lesson_id=lesson_id,
            selected_choice__is_correct=True
        ).count()
        
        total_questions = Question.objects.filter(lesson_id=lesson_id).count()
        
        return Response({
            'score': correct_answers,
            'total': total_questions,
            'percentage': (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        })
    

class CourseQuizResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        course_id = request.query_params.get('course')

        if not course_id:
            return Response({'error': 'يرجى تحديد رقم الكورس'}, status=400)

        questions = Question.objects.filter(lesson__course_id=course_id)
        total_questions = questions.count()

        correct_answers = UserAnswer.objects.filter(
            user=request.user,
            question__in=questions,
            selected_choice__is_correct=True
        ).count()

        percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        return Response({
            'course_id': course_id,
            'score': correct_answers,
            'total': total_questions,
            'percentage': round(percentage, 2)
        })

class SubmitQuizView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        lesson_id = request.data.get('lesson_id')
        user = request.user

        if not lesson_id:
            return Response({'detail': 'يرجى تحديد الدرس.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({'detail': 'الدرس غير موجود.'}, status=status.HTTP_404_NOT_FOUND)

        questions = Question.objects.filter(lesson=lesson)
        total_questions = questions.count()
        correct_answers = 0

        for question in questions:
            try:
                user_answer = UserAnswer.objects.get(user=user, question=question)
                if user_answer.selected_choice.is_correct:
                    correct_answers += 1
            except UserAnswer.DoesNotExist:
                continue  

        score = correct_answers

        result, created = QuizResult.objects.update_or_create(
            user=user,
            lesson=lesson,
            defaults={
                'score': score,
                'total_questions': total_questions
            }
        )

        serializer = QuizResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
