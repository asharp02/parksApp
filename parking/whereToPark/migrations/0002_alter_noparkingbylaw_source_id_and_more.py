# Generated by Django 4.2.2 on 2023-10-02 17:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("whereToPark", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="noparkingbylaw",
            name="source_id",
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name="restrictedparkingbylaw",
            name="source_id",
            field=models.IntegerField(unique=True),
        ),
    ]
