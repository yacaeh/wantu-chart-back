# Generated by Django 3.2.7 on 2023-08-28 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_alter_channel_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='video_count',
        ),
    ]
