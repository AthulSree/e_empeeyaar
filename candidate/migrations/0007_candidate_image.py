# Generated by Django 5.0.6 on 2024-06-13 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0006_leaverecords_non_paid_leave_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='image',
            field=models.ImageField(default='', upload_to='photos/'),
            preserve_default=False,
        ),
    ]