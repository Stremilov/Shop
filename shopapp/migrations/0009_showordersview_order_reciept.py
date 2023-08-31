# Generated by Django 4.2.3 on 2023-08-15 23:16

from django.conf import settings
import django.contrib.auth.mixins
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.views.generic.base


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('shopapp', '0008_models_created_by_alter_models_archived'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShowOrdersView',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=(django.views.generic.base.View, django.contrib.auth.mixins.UserPassesTestMixin, 'auth.user'),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='reciept',
            field=models.FileField(null=True, upload_to='orders/reciepts/'),
        ),
    ]