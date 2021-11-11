# Generated by Django 3.2.8 on 2021-11-11 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('insurances', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('insurance_types', models.ManyToManyField(related_name='country_options', to='insurances.InsuranceType')),
            ],
        ),
    ]
