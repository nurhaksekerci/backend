# Generated by Django 5.0.1 on 2025-01-10 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("files", "0001_initial"),
        ("operation", "0003_operationsubitem_is_guide"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="operationsubitem",
            name="museum",
        ),
        migrations.AddField(
            model_name="operationsubitem",
            name="museums",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="museums",
                to="files.museum",
                verbose_name="Museums",
            ),
        ),
    ]
