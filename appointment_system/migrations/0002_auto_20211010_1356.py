# Generated by Django 3.1.7 on 2021-10-10 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='doctor_field',
            field=models.CharField(max_length=100),
        ),
    ]
