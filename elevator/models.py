
from django.db import models


class Elevator(models.Model):
    operational = models.BooleanField(default=True)
    in_maintenance = models.BooleanField(default=False)
    current_floor = models.IntegerField(default=0)
    moving_up = models.BooleanField(default=False)
    moving_down = models.BooleanField(default=False)
    doors_open = models.BooleanField(default=False)

    def __str__(self):
        return f"Elevator {self.id}"


class Request(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    floor = models.IntegerField(default=0)
