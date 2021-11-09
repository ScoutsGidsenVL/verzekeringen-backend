# Generated by Django 3.2.8 on 2021-11-09 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0034_alter_insuranceclaim_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='insuranceclaim',
            options={'permissions': [('can_view_note_and_case_number', 'Administratieve gebruikers kunnen dossiernummer en opmerkingen bekijken'), ('can_add_claim', 'User can add a claim'), ('can_view_claim', 'User can view a claim'), ('can_list_claims', 'User can view a list of claims'), ('can_add_comment', 'User can add a comment to a claim'), ('can_view_comment', 'User can view a comment on a claim'), ('can_add_case_number', 'User can add a case number to a claim'), ('can_view_case_number', 'User can view the case number of a claim'), ('can_view_attachment_filename', 'User can view the filename of a claim attachment')]},
        ),
    ]
