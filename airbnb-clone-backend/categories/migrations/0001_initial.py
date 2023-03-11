# Generated by Django 4.1.7 on 2023-03-11 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=50)),
                (
                    "kind",
                    models.CharField(
                        choices=[("rooms", "Rooms"), ("experiences", "Experiences")],
                        max_length=15,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
