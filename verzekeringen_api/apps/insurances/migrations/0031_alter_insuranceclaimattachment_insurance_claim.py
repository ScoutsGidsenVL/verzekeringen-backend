# Generated by Django 3.2.5 on 2021-10-11 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0030_auto_20211010_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuranceclaimattachment',
            name='insurance_claim',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachment', to='insurances.insuranceclaim'),
        ),
    ]
