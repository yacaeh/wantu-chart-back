# Generated by Django 3.2.7 on 2023-11-19 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0035_alter_movie_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dailyview',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='dailyview',
            table='daily_views',
        ),
    ]
