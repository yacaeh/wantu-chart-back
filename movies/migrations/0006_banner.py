# Generated by Django 3.2.7 on 2023-08-17 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_rating_spoiler'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('subtitle', models.CharField(max_length=500)),
                ('link', models.CharField(max_length=500)),
                ('order', models.IntegerField()),
                ('type', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
