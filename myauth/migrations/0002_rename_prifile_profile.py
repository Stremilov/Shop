# Generated by Django 4.2.3 on 2023-08-08 11:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Prifile',
            new_name='Profile',
        ),
    ]
