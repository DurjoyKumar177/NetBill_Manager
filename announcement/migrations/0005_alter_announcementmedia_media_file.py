# Generated by Django 5.1 on 2025-01-30 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0004_remove_comment_title_announcement_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcementmedia',
            name='media_file',
            field=models.FileField(upload_to='announcement/media/'),
        ),
    ]
