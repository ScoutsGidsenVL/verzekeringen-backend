# Generated by Django 3.2.9 on 2022-01-05 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scouts_auth', '0002_auto_20211230_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoutsuser',
            name='customer_number',
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
        migrations.AlterField(
            model_name='scoutsuser',
            name='membership_number',
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
        migrations.AlterField(
            model_name='scoutsuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
    ]
