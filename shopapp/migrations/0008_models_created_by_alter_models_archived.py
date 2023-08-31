# Generated by Django 4.2.3 on 2023-08-11 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopapp', '0007_models_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='models',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='models',
            name='archived',
            field=models.BooleanField(default=0),
        ),
    ]
