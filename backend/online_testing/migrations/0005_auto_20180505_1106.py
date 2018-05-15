# Generated by Django 2.0.3 on 2018-05-05 03:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('online_testing', '0004_auto_20180505_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examination',
            name='answers',
            field=models.FileField(default=None, null=True, upload_to='answers/'),
        ),
        migrations.AlterField(
            model_name='examination',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='paper',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 5, 3, 6, 52, 856919, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='paper',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 5, 3, 6, 52, 856919, tzinfo=utc)),
        ),
    ]