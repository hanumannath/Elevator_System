from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Elevator, Request
from .serializers import ElevatorSerializer, RequestSerializer
from django.core.cache import cache


class ElevatorViewSet(viewsets.ViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer
    #This api initialize elevator system with given number of elevators

    def create(self, request):
        num_elevators = int(request.data.get('num_elevators', 0))
        elevators = []
        for i in range(num_elevators):
            elevator = Elevator.objects.create()
            elevators.append(elevator)

        serializer = ElevatorSerializer(elevators, many=True)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=['get'])
    def moving_direction(self, request, pk=None):
        queryset = self.get_queryset()
        elevator = self.get_object(queryset=queryset, pk=pk)

        if elevator.moving_up:
            direction = 'up'
        elif elevator.moving_down:
            direction = 'down'
        else:
            direction = 'stopped'

        return Response({'direction': direction})

    @action(detail=True, methods=['post'])
    def mark_maintenance(self, request, pk=None):
        queryset = self.get_queryset()
        elevator = self.get_object(queryset=queryset, pk=pk)
        in_maintenance = request.data.get('in_maintenance', False)

        elevator.in_maintenance = in_maintenance
        elevator.operational = not in_maintenance
        elevator.save()

        serializer = ElevatorSerializer(elevator)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def door_action(self, request, pk=None):
        queryset = self.get_queryset()
        elevator = self.get_object(queryset=queryset, pk=pk)
        door_action = request.data.get('door_action', 'close')

        if door_action == 'open':
            elevator.doors_open = True
        elif door_action == 'close':
            elevator.doors_open = False
        else:
            return Response({"detail": "Invalid door action"}, status=400)

        elevator.save()

        serializer = ElevatorSerializer(elevator)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def next_destination(self, request, pk=None):
        queryset = self.get_queryset()
        elevator = self.get_object(queryset=queryset, pk=pk)
        current_floor = elevator.current_floor
        moving_up = elevator.moving_up
        moving_down = elevator.moving_down

        # Retrieve all the requests for the elevator and filter them based on the elevator's direction
        if moving_up:
            requests = Request.objects.filter(elevator=elevator, floor__gte=current_floor).order_by('floor')
        elif moving_down:
            requests = Request.objects.filter(elevator=elevator, floor__lte=current_floor).order_by('-floor')
        else:
            requests = Request.objects.filter(elevator=elevator).order_by('floor')

        if requests.exists():
            next_floor = requests.first().floor
        else:
            next_floor = None

        return Response({'next_destination_floor': next_floor})

    @action(detail=True, methods=['post'])
    def set_current_floor(self, request, pk=None):
        elevator = self.get_object(pk=pk)
        current_floor = request.data.get('current_floor')

        if not current_floor:
            return Response({'detail': 'Current floor is required.'}, status=status.HTTP_400_BAD_REQUEST)

        elevator.current_floor = current_floor
        elevator.save()

        return Response({'detail': 'Current floor updated successfully.'}, status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.queryset

    def get_object(self, queryset=None, **kwargs):
        queryset = queryset or self.get_queryset()
        return queryset.get(**kwargs)


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    #this api fetch all the requests for a given elevator id

    def list(self, request):
        elevator_id = request.query_params.get('elevator_id')
        cache_key = f'elevator_data_{elevator_id}'
        data = cache.get(cache_key)
        if data:
            return Response(data)
        queryset = self.queryset.filter(elevator_id=elevator_id)
        serializer = self.serializer_class(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=3600)
        return Response(serializer.data)
   #this api creates a request for a given elevator with a given floor no.

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
