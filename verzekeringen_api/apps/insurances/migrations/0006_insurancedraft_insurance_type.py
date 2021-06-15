# Generated by Django 3.2.4 on 2021-06-15 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0005_auto_20210615_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurancedraft',
            name='insurance_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='insurance_drafts', to='insurances.insurancetype'),
            preserve_default=False,
        ),
    ]
