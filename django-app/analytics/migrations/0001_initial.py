# Generated by Django 4.1.1 on 2022-11-03 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unsubscribed_users', models.IntegerField(default=0)),
            ],
        ),
    ]
