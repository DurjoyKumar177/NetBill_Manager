# Generated by Django 5.1 on 2025-01-29 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complains', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complain',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='complains/complain_attachments/'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='complains/reply_attachments/'),
        ),
    ]
