# Generated by Django 3.2.13 on 2022-05-23 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_job_on_moderation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]
