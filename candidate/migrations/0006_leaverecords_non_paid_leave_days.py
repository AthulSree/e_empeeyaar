# Generated by Django 5.0.6 on 2024-06-11 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0005_rename_leave_days_leaverecords_paid_leave_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverecords',
            name='non_paid_leave_days',
            field=models.CharField(default='', max_length=50),
        ),
    ]
