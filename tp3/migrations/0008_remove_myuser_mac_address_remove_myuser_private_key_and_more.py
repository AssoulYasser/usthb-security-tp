# Generated by Django 4.0 on 2023-12-13 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tp3', '0007_myuser_private_key_myuser_public_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='mac_address',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='private_key',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='public_key',
        ),
    ]
