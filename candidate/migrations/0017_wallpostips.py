# Generated by Django 5.0.6 on 2024-07-11 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0016_wallpost_send_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='wallpostIPs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('group', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'wall_post_ip',
            },
        ),
    ]
