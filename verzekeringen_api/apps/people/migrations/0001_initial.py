# Generated by Django 3.2.9 on 2021-11-29 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.constraints
import django.db.models.deletion
import scouts_auth.inuits.models.fields.django_shorthand_model_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('scouts_insurances', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InuitsNonMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=25)),
                ('phone_number', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=24)),
                ('cell_number', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=24)),
                ('email', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalEmailField(blank=True, max_length=128)),
                ('birth_date', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalDateField(blank=True, null=True)),
                ('gender', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other'), ('U', 'Unknown')], default='U', max_length=1)),
                ('street', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=100)),
                ('number', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=5)),
                ('letter_box', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=5)),
                ('postal_code', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
                ('city', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=40)),
                ('comment', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=500)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='people_inuitsnonmember_created', to=settings.AUTH_USER_MODEL, verbose_name='Instance created by')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='people_inuitsnonmember_updated', to=settings.AUTH_USER_MODEL, verbose_name='Instance last update by')),
            ],
        ),
        migrations.CreateModel(
            name='InuitsNonMemberTemplate',
            fields=[
                ('non_member', models.OneToOneField(db_constraint=django.db.models.constraints.UniqueConstraint, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='scouts_insurances.nonmember')),
                ('inuits_non_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='template', to='people.inuitsnonmember')),
            ],
        ),
        migrations.CreateModel(
            name='InuitsClaimVictim',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=25)),
                ('phone_number', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=24)),
                ('cell_number', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=24)),
                ('email', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalEmailField(blank=True, max_length=128)),
                ('birth_date', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalDateField(blank=True, null=True)),
                ('gender', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other'), ('U', 'Unknown')], default='U', max_length=1)),
                ('street', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=100)),
                ('number', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=5)),
                ('letter_box', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=5)),
                ('postal_code', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
                ('city', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=40)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('legal_representative', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=128)),
                ('group_admin_id', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=64)),
                ('membership_number', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=64)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='people_inuitsclaimvictim_created', to=settings.AUTH_USER_MODEL, verbose_name='Instance created by')),
                ('non_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='claim_victim', to='people.inuitsnonmember')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='people_inuitsclaimvictim_updated', to=settings.AUTH_USER_MODEL, verbose_name='Instance last update by')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
