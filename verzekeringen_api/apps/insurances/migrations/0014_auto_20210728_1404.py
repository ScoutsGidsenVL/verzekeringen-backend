# Generated by Django 3.2.4 on 2021-07-28 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0013_insuranceclaim_witness_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='insuranceclaim',
            old_name='person',
            new_name='declarant',
        ),
        migrations.AddField(
            model_name='insuranceclaim',
            name='declarant_city',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='insuranceclaim',
            name='legal_representative',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
