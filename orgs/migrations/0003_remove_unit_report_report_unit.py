# Generated by Django 4.1.1 on 2023-01-23 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0002_unitname_rename_funct_unit_function_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='report',
        ),
        migrations.AddField(
            model_name='report',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orgs.unit'),
        ),
    ]
