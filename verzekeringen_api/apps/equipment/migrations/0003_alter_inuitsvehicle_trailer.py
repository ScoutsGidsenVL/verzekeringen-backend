# Generated by Django 3.2.9 on 2021-12-08 11:59

from django.db import migrations
import scouts_auth.inuits.models.fields.django_shorthand_model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inuitsvehicle',
            name='trailer',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('0', 'Geen'), ('1', 'Aanhangwagen'), ('2', '<750kg'), ('3', '>750kg')], db_column='aanhangwagen', default='VehicleRelatedInsurance.DEFAULT_VEHICLE_TRAILER_OPTION', max_length=1),
        ),
    ]
