# Generated by Django 4.1.1 on 2022-10-24 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcribe', '0008_alter_transcription_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcription',
            name='is_mp3',
            field=models.BooleanField(default=False),
        ),
    ]