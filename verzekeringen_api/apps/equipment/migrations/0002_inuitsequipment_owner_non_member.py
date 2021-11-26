# Generated by Django 3.2.9 on 2021-11-25 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipment', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inuitsequipment',
            name='owner_non_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inuits_equipment', to='people.inuitsnonmember'),
        ),
    ]
