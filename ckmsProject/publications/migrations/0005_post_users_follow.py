# Generated by Django 3.1.5 on 2021-02-10 20:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publications', '0004_auto_20210201_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='users_follow',
            field=models.ManyToManyField(blank=True, related_name='post_follow', to=settings.AUTH_USER_MODEL),
        ),
    ]
