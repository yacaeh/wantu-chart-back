# Generated by Django 3.2.7 on 2023-11-20 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0037_episode_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='dislikeCount',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]
