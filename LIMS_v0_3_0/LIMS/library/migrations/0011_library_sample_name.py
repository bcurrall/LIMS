# Generated by Django 2.1.5 on 2019-07-31 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0019_sample_name'),
        ('library', '0010_remove_library_sample_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='sample_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sample.Sample'),
        ),
    ]
