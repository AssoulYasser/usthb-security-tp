# Generated by Django 4.0 on 2023-12-07 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tp3', '0003_alter_myuser_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='first_name',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(default='Nigga', max_length=20),
            preserve_default=False,
        ),
    ]
