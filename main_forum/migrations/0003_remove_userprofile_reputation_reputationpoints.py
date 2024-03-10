# Generated by Django 4.1 on 2024-03-10 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_forum', '0002_remove_question_excerpt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='reputation',
        ),
        migrations.CreateModel(
            name='ReputationPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reputation', models.IntegerField(default=0)),
                ('date_awarded', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reputation_points', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reputation Point',
                'verbose_name_plural': 'Reputation Points',
            },
        ),
    ]