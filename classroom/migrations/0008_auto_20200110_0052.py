# Generated by Django 3.0.1 on 2020-01-09 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0007_assignments_marks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignments',
            name='marks',
        ),
        migrations.AddField(
            model_name='assignments',
            name='maximumMarks',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='studentassignmentsubmission',
            name='marks',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
