import uuid
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from courses.models import Course
from .models import FinalQuestion, FinalUserAnswer, FinalQuizResult, Certificate
from .serializers import FinalQuestionSerializer, FinalUserAnswerSerializer, FinalQuizResultSerializer, CertificateSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404 
from rest_framework.response import Response
from django.db.models import Avg
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse, FileResponse

# Create your views here.
class FinalQuestionListView(generics.ListAPIView):
    serializer_class = FinalQuestionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id') 
        if course_id:
            return FinalQuestion.objects.filter(course_id=course_id)
        return FinalQuestion.objects.none()


class FinalUserAnswerCreateView(generics.CreateAPIView):
    serializer_class = FinalUserAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={
            'question': request.data.get('question'),
            'selected_choice': request.data.get('selected_choice')
        })
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data['question']
        user = request.user

        if FinalUserAnswer.objects.filter(user=user, question=question).exists():
            return Response({"detail": "لقد أجبت على هذا السؤال من قبل"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=user)

        course = question.course
        total_questions = FinalQuestion.objects.filter(course=course).count()
        user_answers_count = FinalUserAnswer.objects.filter(user=user, question__course=course).count()

        if user_answers_count == total_questions:
            correct_answers = FinalUserAnswer.objects.filter(
                user=user,
                question__course=course,
                selected_choice__is_correct=True
            ).count()

            FinalQuizResult.objects.update_or_create(
                user=user,
                course=course,
                defaults={
                    'score': correct_answers,
                    'total_questions': total_questions
                }
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FinalQuizResultView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        course_id = request.query_params.get('course')
        if not course_id:
            return Response({'detail': 'يرجى تحديد الكورس'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = FinalQuizResult.objects.get(user=request.user, course_id=course_id)
        except FinalQuizResult.DoesNotExist:
            return Response({'detail': 'لا يوجد نتيجة لهذا الكورس'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FinalQuizResultSerializer(result)
        return Response(serializer.data)
    
# courses/views.py

class GenerateCertificateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get('course')

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'الكورس غير موجود'}, status=404)

        final_result = FinalQuizResult.objects.filter(user=user, course=course).first()

        if not final_result:
            return Response({'error': 'لم يتم العثور على نتيجة الفاينال'}, status=404)

        if final_result.score < 60:
            return Response({'error': 'يجب الحصول على 60٪ على الأقل للحصول على الشهادة'}, status=403)

        certificate, created = Certificate.objects.get_or_create(
            user=user,
            course=course,
            defaults={
                'score': final_result.score,
                'certificate_id': str(uuid.uuid4())
            }
        )

        serializer = CertificateSerializer(certificate)
        return Response(serializer.data)


class CertificatePDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        result = FinalQuizResult.objects.filter(user=request.user, course=course).first()

        if not result or result.score < 0.6 * result.total_questions:
            return Response({"message": "الشهادة غير متاحة، لم تحقق النجاح"}, status=403)

        # إنشاء PDF في الذاكرة
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # =============================
        # 🖼️ مكان اللوجو (حط صورة شعارك هنا)
        # =============================
        # مثال: '/path/to/logo.png'
        logo_path = "/path/to/logo.png"  # ← غيّر المسار ده لمسار اللوجو بتاعك
        try:
            p.drawImage(logo_path, x=2 * cm, y=height - 4 * cm, width=4 * cm, height=4 * cm, mask='auto')
        except:
            p.drawString(2 * cm, height - 3 * cm, "🔻 شعارك هنا (اللوجو مش موجود حالياً)")

        # =============================
        # 📝 نص الشهادة
        # =============================
        p.setFont("Helvetica-Bold", 20)
        p.drawCentredString(width / 2, height - 5 * cm, "شهادة إتمام الدورة")

        p.setFont("Helvetica", 14)
        p.drawCentredString(width / 2, height - 7 * cm, f"نشهد بأن {request.user.first_name} {request.user.last_name}")

        p.setFont("Helvetica", 14)
        p.drawCentredString(width / 2, height - 8.5 * cm, f"قد أكمل بنجاح دورة: {course.title}")

        score_str = f"{result.score}/{result.total_questions}"
        p.drawCentredString(width / 2, height - 10 * cm, f"النتيجة: {score_str}")

        date_str = datetime.now().strftime("%Y-%m-%d")
        p.drawCentredString(width / 2, height - 11.5 * cm, f"التاريخ: {date_str}")

        p.setFont("Helvetica-Oblique", 10)
        p.drawCentredString(width / 2, 2 * cm, "تم إنشاء هذه الشهادة تلقائيًا من نظام التدريب")

        # إنهاء وتقديم الشهادة
        p.showPage()
        p.save()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename="certificate.pdf")