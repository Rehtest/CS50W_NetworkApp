# Generated by Django 2.2.12 on 2023-01-21 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20230121_0705'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-timestamp']},
        ),
    ]
