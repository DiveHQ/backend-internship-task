# Generated by Django 4.2.2 on 2023-06-12 16:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entry",
            name="calories",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name="entry",
            name="is_below_daily_calories_threshold",
            field=models.BooleanField(),
        ),
    ]
