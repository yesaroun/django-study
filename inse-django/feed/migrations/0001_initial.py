# Generated by Django 4.1.4 on 2023-01-04 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('imgs', models.ImageField(blank=True, null=True, upload_to='')),
                ('like', models.PositiveIntegerField()),
                ('content', models.TextField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
