# Generated by Django 4.0.5 on 2022-06-06 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lodge_app', '0020_rename_rerservation_code_reservation_reservation_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_menitiest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='lodge_app.amenity'),
        ),
    ]