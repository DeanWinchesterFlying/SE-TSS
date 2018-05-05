# Generated by Django 2.0.3 on 2018-05-02 12:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('online_testing', '0005_auto_20180502_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examination',
            name='begin',
        ),
        migrations.AlterField(
            model_name='examination',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 2, 12, 34, 33, 386686, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='paper',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 2, 12, 34, 33, 386686, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='paper',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 2, 12, 34, 33, 386686, tzinfo=utc)),
        ),
    ]