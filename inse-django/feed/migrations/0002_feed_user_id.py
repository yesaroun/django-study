# Generated by Django 4.1.4 on 2023-01-03 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
