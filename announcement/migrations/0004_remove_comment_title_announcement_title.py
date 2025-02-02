# Generated by Django 5.1 on 2025-01-30 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0003_comment_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='title',
        ),
        migrations.AddField(
            model_name='announcement',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
