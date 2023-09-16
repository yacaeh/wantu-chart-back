# Generated by Django 3.2.7 on 2023-08-28 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_auto_20230817_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='commentCount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='duration',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='likeCount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='viewCount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
