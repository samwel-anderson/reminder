# Generated by Django 4.0.4 on 2022-06-02 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodge_app', '0002_reservation_rejected_alter_reservedroom_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='rerservation_code',
            field=models.IntegerField(default=8258),
        ),
    ]