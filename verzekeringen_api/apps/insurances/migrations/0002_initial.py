# Generated by Django 3.2.9 on 2021-12-24 03:14

import django.db.models.deletion
from django.db import migrations, models

import scouts_auth.inuits.models.fields.django_shorthand_model_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('insurances', '0001_initial'),
        ('scouts_auth', '0001_initial'),
        ('people', '0001_initial'),
        ('scouts_insurances', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuranceclaim',
            name='victim',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.inuitsclaimvictim'),
        ),
        migrations.AddField(
            model_name='eventinsuranceattachment',
            name='file',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='event_insurance', to='scouts_auth.persistedfile'),
        ),
        migrations.AddField(
            model_name='eventinsuranceattachment',
            name='insurance',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachment', to='scouts_insurances.eventinsurance'),
        ),
        migrations.AddField(
            model_name='activityinsuranceattachment',
            name='file',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='activity_insurance', to='scouts_auth.persistedfile'),
        ),
        migrations.AddField(
            model_name='activityinsuranceattachment',
            name='insurance',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='attachment', to='scouts_insurances.activityinsurance'),
        ),
    ]
