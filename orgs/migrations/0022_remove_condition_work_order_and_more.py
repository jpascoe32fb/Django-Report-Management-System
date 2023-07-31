# Generated by Django 4.1.1 on 2023-06-26 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0021_alter_attachment_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='condition',
            name='work_order',
        ),
        migrations.RemoveField(
            model_name='condition',
            name='work_req',
        ),
        migrations.AddField(
            model_name='asset',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='component',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='condition',
            name='data_collection_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='function',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='unitname',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='condition',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='faultgroup',
            name='fault_group',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='comment',
            field=models.CharField(max_length=1200, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='recommendation',
            field=models.CharField(max_length=1200, null=True),
        ),
    ]