# Generated by Django 2.1.5 on 2019-06-21 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_auto_20190205_1302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='library',
            old_name='qpcr_conc',
            new_name='qpcr_conc_molarity_nM',
        ),
        migrations.RenameField(
            model_name='library',
            old_name='qubit_conc',
            new_name='qubit_conc_ng_uL',
        ),
        migrations.RenameField(
            model_name='library',
            old_name='tapestation_conc',
            new_name='tapestation_conc_ng_uL',
        ),
    ]