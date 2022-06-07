# Generated by Django 3.2.9 on 2022-06-07 08:41

from django.db import migrations, models
import scouts_auth.inuits.models.fields.django_shorthand_model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('scouts_insurances', '0017_alter_travelassistanceinsurance_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelassistanceinsurance',
            name='_vehicle_chassis_number',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, db_column='autochassis', max_length=20, null=True),
        ),
    ]
