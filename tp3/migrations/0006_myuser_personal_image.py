# Generated by Django 4.0 on 2023-12-11 13:31

from django.db import migrations, models
import tp3.models


class Migration(migrations.Migration):

    dependencies = [
        ('tp3', '0005_myuser_mac_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='personal_image',
            field=models.ImageField(default=None, upload_to=tp3.models.user_directory_path),
            preserve_default=False,
        ),
    ]
