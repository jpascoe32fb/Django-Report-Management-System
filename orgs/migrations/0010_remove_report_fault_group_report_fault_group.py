# Generated by Django 4.1.1 on 2023-06-01 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0009_remove_faultgroup_name_faultgroup_fault_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='fault_group',
        ),
        migrations.AddField(
            model_name='report',
            name='fault_group',
            field=models.ManyToManyField(blank=True, null=True, to='orgs.faultgroup'),
        ),
    ]
