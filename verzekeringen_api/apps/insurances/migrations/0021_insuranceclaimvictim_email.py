# Generated by Django 3.2.5 on 2021-08-09 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0020_auto_20210809_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuranceclaimvictim',
            name='email',
            field=models.EmailField(blank=True, max_length=60),
        ),
    ]