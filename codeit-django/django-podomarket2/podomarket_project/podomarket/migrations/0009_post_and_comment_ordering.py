# Generated by Django 2.2 on 2023-07-02 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('podomarket', '0008_like'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['dt_created']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-dt_created']},
        ),
    ]
