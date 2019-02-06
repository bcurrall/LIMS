# Generated by Django 2.1.5 on 2019-02-06 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_auto_20190205_1302'),
        ('sequence', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wusubmission',
            name='walk_up_submission_name',
        ),
        migrations.AddField(
            model_name='wusubmission',
            name='pool_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='library.Pool'),
        ),
        migrations.AddField(
            model_name='wusubmission',
            name='wus_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]