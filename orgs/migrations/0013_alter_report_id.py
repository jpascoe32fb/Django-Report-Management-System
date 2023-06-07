# Generated by Django 4.1.1 on 2023-06-01 20:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0012_alter_report_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]