# Generated by Django 3.2.7 on 2023-08-02 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='average_rating',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=2, null=True),
        ),
    ]
