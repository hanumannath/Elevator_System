# Generated by Django 4.2.1 on 2023-05-26 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Elevator",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("operational", models.BooleanField(default=True)),
                ("in_maintenance", models.BooleanField(default=False)),
                ("current_floor", models.IntegerField(default=0)),
                ("moving_up", models.BooleanField(default=False)),
                ("moving_down", models.BooleanField(default=False)),
                ("doors_open", models.BooleanField(default=False)),
            ],
        ),
    ]
