# Generated by Django 3.2.13 on 2022-05-24 16:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20220524_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='job',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
