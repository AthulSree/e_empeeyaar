# Generated by Django 5.0.6 on 2024-06-08 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('c_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('designation', models.CharField(max_length=200)),
                ('joining_date', models.DateField()),
                ('project_no', models.CharField(max_length=20)),
                ('workorder_no', models.CharField(max_length=20)),
                ('entered_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'candidates',
            },
        ),
    ]
