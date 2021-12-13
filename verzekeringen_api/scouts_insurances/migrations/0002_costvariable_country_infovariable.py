# Generated by Django 3.2.9 on 2021-12-08 12:22

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scouts_insurances', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoVariable',
            fields=[
                ('key', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('insurance_types', models.ManyToManyField(related_name='country_options', to='scouts_insurances.InsuranceType')),
            ],
        ),
        migrations.CreateModel(
            name='CostVariable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=30)),
                ('value', models.DecimalField(decimal_places=5, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
                ('insurance_type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cost_variables', to='scouts_insurances.insurancetype')),
            ],
            options={
                'unique_together': {('key', 'insurance_type')},
            },
        ),
    ]