# Generated by Django 2.1.5 on 2019-08-22 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0023_pool_batch_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pool',
            name='batch_id',
        ),
        migrations.AddField(
            model_name='pool',
            name='batch_id_2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='pool name2'),
        ),
    ]