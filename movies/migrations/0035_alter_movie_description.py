# Generated by Django 3.2.7 on 2023-11-19 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0034_auto_20231120_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
