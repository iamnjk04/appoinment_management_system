# Generated by Django 3.1.7 on 2021-10-11 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment_system', '0002_auto_20211010_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='managed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='admin_of', to=settings.AUTH_USER_MODEL),
        ),
    ]
