# Generated by Django 2.0.3 on 2018-04-28 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20180429_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='id_number',
            field=models.CharField(default='null', max_length=18, unique=True, verbose_name='身份证号'),
        ),
    ]
