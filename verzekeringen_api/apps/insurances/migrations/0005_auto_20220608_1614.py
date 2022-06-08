# Generated by Django 3.2.9 on 2022-06-08 14:14

from django.db import migrations
import scouts_auth.inuits.models.fields.django_shorthand_model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0004_insuranceclaim_attachment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insuranceclaim',
            name='involved_party',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='insuranceclaim',
            name='leadership',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='insuranceclaim',
            name='official_report',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='insuranceclaim',
            name='witness',
            field=scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=30, null=True),
        ),
    ]
