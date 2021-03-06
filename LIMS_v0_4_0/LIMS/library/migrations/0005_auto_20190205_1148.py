# Generated by Django 2.1.5 on 2019-02-05 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20190205_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='PoolingAmounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rel_proportion', models.CharField(max_length=100)),
                ('amount_of_library_used', models.FloatField(blank=True, default=0, null=True)),
                ('library_amount', models.CharField(blank=True, max_length=100, null=True)),
                ('library_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='library.Library')),
            ],
        ),
        migrations.RemoveField(
            model_name='pool',
            name='amount_of_library_used',
        ),
        migrations.RemoveField(
            model_name='pool',
            name='library_amount',
        ),
        migrations.RemoveField(
            model_name='pool',
            name='library_name',
        ),
        migrations.RemoveField(
            model_name='pool',
            name='rel_proportion',
        ),
        migrations.AddField(
            model_name='poolingamounts',
            name='pool_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='library.Pool'),
        ),
    ]
