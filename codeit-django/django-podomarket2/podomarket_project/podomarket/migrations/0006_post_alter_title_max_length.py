# Generated by Django 2.2 on 2023-06-22 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podomarket', '0005_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]