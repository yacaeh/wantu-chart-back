# Generated by Django 3.2.7 on 2023-07-29 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=45)),
                ('password', models.CharField(max_length=500)),
                ('introduction', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
