# Generated by Django 3.2.7 on 2023-11-09 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0027_alter_episode_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='total_dislikes',
            field=models.BigIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='total_videos',
            field=models.BigIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='wantu_score',
            field=models.BigIntegerField(default=0, null=True),
        ),
    ]
