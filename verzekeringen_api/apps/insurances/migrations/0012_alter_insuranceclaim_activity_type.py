# Generated by Django 3.2.4 on 2021-07-14 08:25

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0011_alter_insuranceclaim_activity_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuranceclaim',
            name='activity_type',
            field=jsonfield.fields.JSONField(max_length=128),
        ),
    ]