# Generated by Django 5.0.6 on 2024-08-29 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0021_wallpost_seen'),
    ]

    operations = [
        migrations.CreateModel(
            name='wallpostAccessRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_active_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate.wallpostips')),
            ],
            options={
                'db_table': 'wallpost_access_records',
            },
        ),
    ]
