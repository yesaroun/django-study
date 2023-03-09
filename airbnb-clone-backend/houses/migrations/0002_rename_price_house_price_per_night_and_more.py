# Generated by Django 4.1.7 on 2023-03-08 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("houses", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="house",
            old_name="price",
            new_name="price_per_night",
        ),
        migrations.AddField(
            model_name="house",
            name="pets_allowed",
            field=models.BooleanField(default=True),
        ),
    ]
