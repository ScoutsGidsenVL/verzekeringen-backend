# Generated by Django 3.2.8 on 2021-11-02 17:12

from django.db import migrations, models
import inuits.models.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('scouts_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAdminAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_admin_id', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('street', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('number', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('letter_box', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('postal_code', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('city', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('country', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('phone', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('status', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('giscode', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('description', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupAdminContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('function', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('name', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('phone', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('email', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupAdminLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rel', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('href', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('method', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupAdminMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other'), ('U', 'Unknown')], default='U', max_length=1)),
                ('phone_number', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('first_name', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('last_name', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('birth_date', inuits.models.fields.OptionalDateField(blank=True, null=True)),
                ('membership_number', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('customer_number', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('email', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('username', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('group_admin_id', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MemberList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', inuits.models.fields.OptionalIntegerField(blank=True, null=True)),
                ('total', inuits.models.fields.OptionalIntegerField(blank=True, null=True)),
                ('offset', inuits.models.fields.OptionalIntegerField(blank=True, null=True)),
                ('filter_criterium', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MemberListMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_admin_id', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('index', inuits.models.fields.OptionalIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScoutsFunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('function', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('begin', inuits.models.fields.OptionalDateTimeField(blank=True, null=True)),
                ('code', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('description', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScoutsGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_admin_id', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('number', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('name', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('bank_account', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('email', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('website', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('info', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
                ('type', inuits.models.fields.OptionalCharField(blank=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='ScoutsAuthGroup',
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
