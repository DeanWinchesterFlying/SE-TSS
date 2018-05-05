# Generated by Django 2.0.3 on 2018-05-02 07:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('online_testing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='examination',
            name='begin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='examination',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 2, 7, 52, 26, 226086, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='paper',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 2, 7, 52, 26, 225086, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='paper',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 2, 7, 52, 26, 225086, tzinfo=utc)),
        ),
    ]
