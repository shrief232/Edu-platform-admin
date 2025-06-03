from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False) 
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email','is_instructor', 'is_student', 'language_preference', 'phone_number', 'company_name', 'job_title', 'profile_image','last_login', 'date_joined', 'is_active')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user

