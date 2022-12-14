# Generated by Django 4.1.1 on 2022-09-30 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcribe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcription',
            name='transcribed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transcription',
            name='audio',
            field=models.FileField(upload_to='uploads/%Y/%m/%d'),
        ),
    ]
