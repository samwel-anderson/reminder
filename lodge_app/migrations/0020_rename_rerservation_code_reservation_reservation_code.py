# Generated by Django 4.0.5 on 2022-06-05 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lodge_app', '0019_alter_reservation_rerservation_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='rerservation_code',
            new_name='reservation_code',
        ),
    ]
