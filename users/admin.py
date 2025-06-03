from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailVerification

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'is_instructor', 'is_student', 'phone_number', 'is_active'
    )
    list_filter = (
        'is_instructor', 'is_active', 'is_staff'
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {
            'fields': (
                'first_name', 'last_name', 'phone_number',
                'company_name', 'job_title', 'profile_image'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'is_instructor', 'is_student', 'groups', 'user_permissions'
            )
        }),
        ('Preferences', {'fields': ('language_preference',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'first_name', 'last_name', 'is_instructor', 'is_student',
                'language_preference', 'is_active', 'is_staff', 'is_superuser',
            ),
        }),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified',)
    search_fields = ('user__email',)
    list_filter = ('is_verified',)
    

admin.site.site_header = "Education Platform"


