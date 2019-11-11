# Generated by Django 2.1.5 on 2019-11-11 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0026_auto_20190910_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='cell_line_type',
            field=models.CharField(blank=True, choices=[('LCL', 'LCL'), ('iN', 'iN'), ('iPS', 'iPS'), ('NPC', 'NPC'), ('NSC', 'NSC'), ('iNeurons', 'iNeurons'), ('fibroblast', 'fibroblast')], max_length=100, null=True),
        ),
    ]