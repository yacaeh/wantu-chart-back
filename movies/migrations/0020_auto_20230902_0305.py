# Generated by Django 3.2.7 on 2023-09-01 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0019_auto_20230828_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='highlightEnd',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='highlightStart',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='topComments',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
