# Generated by Django 4.1.1 on 2023-06-01 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0010_remove_report_fault_group_report_fault_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='fault_group',
            field=models.ManyToManyField(blank=True, to='orgs.faultgroup'),
        ),
    ]
