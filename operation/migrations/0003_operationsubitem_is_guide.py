# Generated by Django 5.0.1 on 2025-01-10 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("operation", "0002_alter_operation_reference_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="operationsubitem",
            name="is_guide",
            field=models.BooleanField(default=False, verbose_name="Is Guide"),
        ),
    ]
