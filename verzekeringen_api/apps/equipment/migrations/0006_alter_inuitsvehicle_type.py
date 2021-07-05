# Generated by Django 3.2.4 on 2021-06-24 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0005_alter_inuitsequipment_nature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inuitsvehicle',
            name='type',
            field=models.CharField(choices=[('PERSONENWAGEN', 'Personenwagen (maximum 5 inzittenden)'), ('MINIBUS', 'Minibus (maximum 8 inzittenden)'), ('VRACHTWAGEN', 'Vrachtwagen tot 3.5 ton (maximum 8 inzittenden)')], max_length=30),
        ),
    ]