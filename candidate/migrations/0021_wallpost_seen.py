# Generated by Django 5.0.6 on 2024-08-28 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0020_remove_wallpost_reply_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallpost',
            name='seen',
            field=models.CharField(default='Y', max_length=1),
            preserve_default=False,
        ),
    ]