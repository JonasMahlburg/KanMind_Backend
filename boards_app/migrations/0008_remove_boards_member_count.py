# Generated by Django 5.2.1 on 2025-06-04 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards_app', '0007_boards_tasks_to_do'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boards',
            name='member_count',
        ),
    ]
