# Generated by Django 3.2.8 on 2021-11-11 16:52

from django.db import migrations, models
import django.db.models.constraints
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('insurances', '0001_initial'),
        ('members', '0001_initial'),
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleInuitsTemplate',
            fields=[
                ('temporary_vehicle_insurance', models.OneToOneField(db_constraint=django.db.models.constraints.UniqueConstraint, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='insurances.temporaryvehicleinsurance')),
                ('inuits_vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.inuitsvehicle')),
            ],
        ),
        migrations.AddField(
            model_name='inuitsequipment',
            name='owner_non_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inuits_equipment', to='members.inuitsnonmember'),
        ),
    ]
