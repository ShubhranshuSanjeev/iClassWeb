# Generated by Django 3.0.1 on 2020-01-14 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Answer')),
                ('submissionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.QuizSubmission')),
            ],
        ),
    ]
