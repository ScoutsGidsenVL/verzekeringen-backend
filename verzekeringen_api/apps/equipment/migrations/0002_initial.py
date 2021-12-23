# Generated by Django 3.2.9 on 2021-12-23 11:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipment', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inuitsequipment',
            name='owner_non_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inuits_equipment', to='people.inuitsnonmember'),
        ),
        migrations.AddField(
            model_name='inuitsequipment',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipment_inuitsequipment_updated', to=settings.AUTH_USER_MODEL, verbose_name='Instance last update by'),
        ),
    ]
