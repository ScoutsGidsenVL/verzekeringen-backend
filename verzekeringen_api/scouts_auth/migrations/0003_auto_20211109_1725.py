# Generated by Django 3.2.8 on 2021-11-09 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scouts_auth', '0002_auto_20211102_1812'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GroupAdminAddress',
        ),
        migrations.DeleteModel(
            name='GroupAdminContact',
        ),
        migrations.DeleteModel(
            name='GroupAdminLink',
        ),
        migrations.DeleteModel(
            name='GroupAdminMember',
        ),
        migrations.DeleteModel(
            name='MemberList',
        ),
        migrations.DeleteModel(
            name='MemberListMember',
        ),
        migrations.DeleteModel(
            name='ScoutsFunction',
        ),
        migrations.DeleteModel(
            name='ScoutsGroup',
        ),
    ]
