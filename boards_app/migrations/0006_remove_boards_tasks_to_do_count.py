# Generated by Django 5.2.1 on 2025-06-03 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards_app', '0005_alter_boards_tasks_to_do_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boards',
            name='tasks_to_do_count',
        ),
    ]
