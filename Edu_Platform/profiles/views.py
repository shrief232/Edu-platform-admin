from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import UserCourseProfile
from .serializers import UserCourseProfileSerializer


class UserCourseProfileView(generics.RetrieveAPIView):
    serializer_class = UserCourseProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        course_id = self.kwargs['course_id']
        return get_object_or_404(
            UserCourseProfile,
            user=self.request.user,
            course_id=course_id
        )

class UserCourseProfileListView(generics.ListAPIView):
    serializer_class = UserCourseProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserCourseProfile.objects.filter(user=self.request.user)    