# Generated by Django 5.0.6 on 2024-08-23 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Docsquad', '0009_alter_docsquad_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='docsquad',
            name='file_path',
            field=models.FileField(null=True, upload_to='docsquad/'),
        ),
    ]
