# Generated by Django 4.1.4 on 2023-01-03 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_feed_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='content',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='feed',
            name='img',
            field=models.ImageField(upload_to=''),
        ),
    ]
