# Generated by Django 4.1.1 on 2022-11-03 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_signintoken_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='signintoken',
            name='create_datetime',
            field=models.DateTimeField(auto_now_add=True, default='2022-01-01 10:10'),
            preserve_default=False,
        ),
    ]
