# elevator/admin.py
from django.contrib import admin
from .models import *


class ElevatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'operational', 'in_maintenance', 'current_floor', 'moving_up', 'moving_down', 'doors_open')
    search_fields = ('id', 'current_floor')


admin.site.register(Elevator)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('elevator', 'floor')

# admin.site.register(Elevator, ElevatorAdmin)
# admin.site.register(Request, ElevatorAdmin)