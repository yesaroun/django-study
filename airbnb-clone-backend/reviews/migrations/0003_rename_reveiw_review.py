# Generated by Django 4.1.7 on 2023-03-21 08:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rooms", "0006_rename_categories_room_category"),
        (
            "experiences",
            "0004_alter_experience_category_alter_experience_host_and_more",
        ),
        ("reviews", "0002_alter_reveiw_experiences_alter_reveiw_room_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Reveiw",
            new_name="Review",
        ),
    ]