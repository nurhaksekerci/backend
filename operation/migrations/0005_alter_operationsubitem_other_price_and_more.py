# Generated by Django 5.0.1 on 2025-01-12 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
        ("operation", "0004_remove_operationsubitem_museum_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="operationsubitem",
            name="other_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="Other Price",
            ),
        ),
        migrations.AlterField(
            model_name="operationsubitem",
            name="other_price_currency",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="authentication.currency",
                verbose_name="Other Price Currency",
            ),
        ),
    ]
