from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
# from unfold.admin import site as unfold_site


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns (
    path("admin/", admin.site.urls),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('notifications/', include('notifications.urls')),
    path('final/', include('final.urls')),
    path('profiles/', include('profiles.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)