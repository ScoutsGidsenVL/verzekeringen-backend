# Generated by Django 3.2.4 on 2021-06-15 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('insurances', '0004_insurancedraft_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='insurancedraft',
            old_name='created_at',
            new_name='created_on',
        ),
        migrations.AddField(
            model_name='insurancedraft',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='insurance_draft_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
    ]
