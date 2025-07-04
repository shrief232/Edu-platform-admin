# Generated by Django 4.2.16 on 2025-05-18 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_questions', to='courses.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_questions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LessonAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='courses.lessonquestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_answers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
