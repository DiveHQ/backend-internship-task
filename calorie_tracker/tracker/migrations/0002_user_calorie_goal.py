# Generated by Django 4.0.4 on 2023-06-19 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='calorie_goal',
            field=models.IntegerField(default=2000),
        ),
    ]
