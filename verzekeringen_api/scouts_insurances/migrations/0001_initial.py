# Generated by Django 3.2.9 on 2021-12-24 03:14

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import scouts_auth.inuits.models.fields.datetype_aware_date_field
import scouts_auth.inuits.models.fields.django_shorthand_model_fields
import scouts_auth.inuits.models.fields.timezone_aware_date_time_field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(db_column='adres_id', primary_key=True, serialize=False)),
                ('street', models.CharField(db_column='straat', max_length=100)),
                ('number', models.CharField(db_column='nummer', max_length=5)),
                ('letter_box', models.CharField(blank=True, db_column='bus', max_length=5, null=True)),
                ('postal_code', models.CharField(db_column='postcode', max_length=4)),
                ('city', models.CharField(db_column='gemeente', max_length=40)),
            ],
            options={
                'db_table': 'vrzk_adres',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BaseInsurance',
            fields=[
                ('id', models.AutoField(db_column='verzekeringsid', primary_key=True, serialize=False)),
                ('_status', models.IntegerField(blank=True, db_column='status', null=True)),
                ('invoice_number', models.IntegerField(blank=True, db_column='factuurnr', null=True)),
                ('invoice_date', scouts_auth.inuits.models.fields.timezone_aware_date_time_field.TimezoneAwareDateTimeField(blank=True, db_column='facturatiedatum', null=True)),
                ('_group_group_admin_id', models.CharField(db_column='groepsnr', max_length=6)),
                ('_group_name', models.CharField(db_column='groepsnaam', max_length=50)),
                ('_group_location', models.CharField(db_column='groepsplaats', max_length=50)),
                ('total_cost', models.DecimalField(db_column='totkostprijs', decimal_places=2, max_digits=7, null=True)),
                ('comment', models.CharField(blank=True, db_column='opmerking', max_length=500)),
                ('vvksm_comment', models.CharField(blank=True, db_column='vvksmopmerking', max_length=500)),
                ('_printed', models.CharField(db_column='afgedrukt', default='N', max_length=1)),
                ('_finished', models.CharField(db_column='afgewerkt', default='N', max_length=1)),
                ('_listed', models.CharField(db_column='lijstok', default='N', max_length=1)),
                ('created_on', scouts_auth.inuits.models.fields.timezone_aware_date_time_field.TimezoneAwareDateTimeField(db_column='datumvaninvulling', null=True)),
                ('start_date', scouts_auth.inuits.models.fields.timezone_aware_date_time_field.TimezoneAwareDateTimeField(db_column='begindatum', null=True)),
                ('end_date', scouts_auth.inuits.models.fields.timezone_aware_date_time_field.TimezoneAwareDateTimeField(db_column='einddatum', null=True)),
                ('payment_date', scouts_auth.inuits.models.fields.timezone_aware_date_time_field.TimezoneAwareDateTimeField(blank=True, db_column='betalingsdatum', null=True)),
            ],
            options={
                'db_table': 'vrzkverzekeringen',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(db_column='materiaalid', primary_key=True, serialize=False)),
                ('nature', models.CharField(blank=True, db_column='aard', max_length=50)),
                ('description', models.CharField(db_column='materieomschrijving', max_length=500)),
                ('amount', models.IntegerField(db_column='aantal', default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('total_value', models.DecimalField(db_column='nieuwwaardeperstuk', decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
            ],
            options={
                'db_table': 'vrzkmateriaal',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InsuranceType',
            fields=[
                ('id', models.IntegerField(db_column='verzekeringstypeid', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='verzekeringstype', max_length=30)),
                ('description', models.CharField(db_column='verzekeringstypeomschr', max_length=50)),
                ('max_term', models.CharField(db_column='maxtermijn', max_length=10)),
            ],
            options={
                'db_table': 'vrzkverzekeringstypes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('last_name', models.CharField(db_column='naam', max_length=25)),
                ('first_name', models.CharField(db_column='voornaam', max_length=15)),
                ('phone_number', models.CharField(blank=True, db_column='telefoon', max_length=15)),
                ('birth_date', scouts_auth.inuits.models.fields.datetype_aware_date_field.DatetypeAwareDateField(blank=True, db_column='geboortedatum', null=True)),
                ('id', models.AutoField(db_column='lidid', primary_key=True, serialize=False)),
                ('membership_number', models.BigIntegerField(db_column='lidnr')),
                ('email', models.EmailField(blank=True, max_length=60)),
                ('group_admin_id', models.CharField(blank=True, db_column='ga_id', max_length=255)),
            ],
            options={
                'db_table': 'vrzkleden',
                'ordering': ['id'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NonMember',
            fields=[
                ('last_name', models.CharField(db_column='naam', max_length=25)),
                ('first_name', models.CharField(db_column='voornaam', max_length=15)),
                ('phone_number', models.CharField(blank=True, db_column='telefoon', max_length=15)),
                ('birth_date', scouts_auth.inuits.models.fields.datetype_aware_date_field.DatetypeAwareDateField(blank=True, db_column='geboortedatum', null=True)),
                ('id', models.AutoField(db_column='nietlidid', primary_key=True, serialize=False)),
                ('street', models.CharField(blank=True, db_column='straat', max_length=100)),
                ('number', models.CharField(blank=True, db_column='nr', max_length=5)),
                ('letter_box', models.CharField(blank=True, db_column='bus', max_length=5)),
                ('postal_code', models.IntegerField(blank=True, db_column='postcode', null=True)),
                ('city', models.CharField(blank=True, db_column='gemeente', max_length=40)),
                ('comment', models.CharField(blank=True, db_column='commentaar', max_length=500)),
            ],
            options={
                'db_table': 'vrzknietleden',
                'ordering': ['id'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InfoVariable',
            fields=[
                ('key', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ActivityInsurance',
            fields=[
                ('insurance_parent', models.OneToOneField(db_column='verzekeringsid', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='activity_child', serialize=False, to='scouts_insurances.baseinsurance')),
                ('nature', models.CharField(db_column='aardactiviteit', max_length=500)),
                ('group_size', models.IntegerField(db_column='aantgroep', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9)])),
                ('postal_code', models.IntegerField(db_column='postcode', null=True)),
                ('city', models.CharField(db_column='gemeente', max_length=40)),
            ],
            options={
                'db_table': 'vrzktypeeenact',
                'managed': False,
            },
            bases=('scouts_insurances.baseinsurance',),
        ),
        migrations.CreateModel(
            name='EquipmentInsurance',
            fields=[
                ('insurance_parent', models.OneToOneField(db_column='verzekeringsid', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='equipment_child', serialize=False, to='scouts_insurances.baseinsurance')),
                ('nature', models.CharField(db_column='aardactiviteit', max_length=500)),
                ('postal_code', models.IntegerField(blank=True, db_column='postcode', null=True)),
                ('city', models.CharField(blank=True, db_column='gemeente', max_length=40)),
                ('_country', models.CharField(blank=True, db_column='land', max_length=45)),
            ],
            options={
                'db_table': 'vrzktypemateriaal',
                'managed': False,
            },
            bases=('scouts_insurances.baseinsurance',),
        ),
        migrations.CreateModel(
            name='EventInsurance',
            fields=[
                ('insurance_parent', models.OneToOneField(db_column='verzekeringsid', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='event_child', serialize=False, to='scouts_insurances.baseinsurance')),
                ('nature', models.CharField(db_column='aardactiviteit', max_length=500)),
                ('event_size', models.IntegerField(choices=[(1, '1-500 (65,55 eur/dag)'), (2, '500-1000 (131,10 eur/dag)'), (3, '1000-1500 (163,88 eur/dag)'), (4, '1500-2500 (229,43 eur/dag)'), (5, 'meer dan 2500 (in overleg met Ethias)')], db_column='aantbezoekers', null=True)),
                ('postal_code', models.IntegerField(db_column='postcode', null=True)),
                ('city', models.CharField(db_column='gemeente', max_length=40)),
            ],
            options={
                'db_table': 'vrzktypeevenement',
                'managed': False,
            },
            bases=('scouts_insurances.baseinsurance',),
        ),
        migrations.CreateModel(
            name='NonMemberTemporaryInsurance',
            fields=[
                ('non_member_id', models.ForeignKey(db_column='nietledenid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='temporary', serialize=False, to='scouts_insurances.nonmember')),
            ],
            options={
                'db_table': 'vrzknietledentijd',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantTemporaryVehicleInsurance',
            fields=[
                ('participant', models.ForeignKey(db_column='bestuurderid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='temporary_vehicle', serialize=False, to='scouts_insurances.nonmember')),
                ('type', models.CharField(choices=[('Bestuurder', 'Bestuurder'), ('Eigenaar', 'Eigenaar')], db_column='soort', max_length=10)),
            ],
            options={
                'db_table': 'vrzktijdautonietleden',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantTravelAssistanceInsurance',
            fields=[
                ('participant', models.ForeignKey(db_column='passagierid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='travel', serialize=False, to='scouts_insurances.nonmember')),
            ],
            options={
                'db_table': 'vrzkassistpassagier',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TemporaryInsurance',
            fields=[
                ('insurance_parent', models.OneToOneField(db_column='verzekeringsid', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='temporary_child', serialize=False, to='scouts_insurances.baseinsurance')),
                ('nature', models.CharField(db_column='aardactiviteit', max_length=500)),
                ('postal_code', models.IntegerField(blank=True, db_column='postcode', null=True)),
                ('city', models.CharField(blank=True, db_column='gemeente', max_length=40)),
                ('_country', models.CharField(blank=True, db_column='land', max_length=45)),
            ],
            options={
                'db_table': 'vrzktypetijdact',
                'managed': False,
            },
            bases=('scouts_insurances.baseinsurance',),
        ),
        migrations.CreateModel(
            name='TemporaryVehicleInsurance',
            fields=[
                ('_vehicle_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, choices=[('PERSONENWAGEN', 'Personenwagen (maximum 5 inzittenden)'), ('MINIBUS', 'Minibus (maximum 8 inzittenden)'), ('VRACHTWAGEN', 'Vrachtwagen tot 3.5 ton (maximum 8 inzittenden)')], db_column='autotype', max_length=30)),
                ('_vehicle_brand', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, db_column='automerk', max_length=15)),
                ('_vehicle_license_plate', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, db_column='autokenteken', max_length=10)),
                ('_vehicle_construction_year', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, db_column='autobouwjaar', null=True, validators=[django.core.validators.MinValueValidator(1900)])),
                ('_vehicle_chassis_number', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, db_column='autochassis', max_length=20)),
                ('_vehicle_trailer', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, choices=[('0', 'Geen'), ('2', '<750kg'), ('3', '>750kg')], db_column='aanhangwagen', max_length=1)),
                ('insurance_parent', models.OneToOneField(db_column='verzekeringsid', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='temporary_vehicle_child', serialize=False, to='scouts_insurances.baseinsurance')),
                ('insurance_options', models.IntegerField(choices=[(1, 'omnium'), (2, 'reeds afgesloten omnium afdekken'), (3, 'huurvoertuigen'), (13, 'omnium + huurvoertuigen'), (23, 'reeds afgesloten omnium afdekken + huurvoertuigen')], db_column='keuze')),
                ('max_coverage', models.CharField(blank=True, choices=[('A', '247,89 EUR'), ('B', '495,79 EUR'), ('C', '743,68 EUR')], db_column='maxdekking', max_length=1, null=True)),
            ],
            options={
                'db_table': 'vrzktypetijdauto',
                'managed': False,
            },
            bases=('scouts_insurances.baseinsurance', models.Model),
        ),
        migrations.CreateModel(
            name='TravelAssistanceInsurance',
            fields=[
                ('_vehicle_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, choices=[('PERSONENWAGEN', 'Personenwagen (maximum 5 inzittenden)'), ('MINIBUS', 'Minibus (maximum 8 inzittenden)'), ('VRACHTWAGEN', 'Vrachtwagen tot 3.5 ton (maximum 8 inzittenden)')], db_column='autotype', max_length=30)),
                ('_vehicle_brand', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, db_column='automerk', max_length=15)),
                ('_vehicle_license_plate', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, db_column='autokenteken', max_length=10)),
                ('_vehicle_construction_year', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, db_column='autobouwjaar', null=True, validators=[django.core.validators.MinValueValidator(1900)])),
                ('_vehicle_trailer', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, choices=[(0, 'Geen'), (1, 'Aanhangwagen')], db_column='aanhangwagen', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('insurance_parent', models.OneToOneField(db_column='verzekeringsid', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='travel_assistance_child', serialize=False, to='scouts_insurances.baseinsurance')),
                ('country', models.CharField(db_column='bestemmingsland', max_length=40)),
            ],
            options={
                'db_table': 'vrzktypeethiasassistance',
                'managed': False,
            },
            bases=('scouts_insurances.baseinsurance', models.Model),
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
