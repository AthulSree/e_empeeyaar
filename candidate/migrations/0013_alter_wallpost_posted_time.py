# Generated by Django 5.0.6 on 2024-06-27 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0012_wallpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallpost',
            name='posted_time',
            field=models.DateTimeField(),
        ),
    ]
