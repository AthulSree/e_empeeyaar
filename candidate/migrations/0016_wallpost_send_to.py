# Generated by Django 5.0.6 on 2024-07-11 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0015_wallpost_disabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallpost',
            name='send_to',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
