from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import *
from .models import *


class ElevatorViewSet(viewsets.ViewSet):
    def create(self, request):
        num_elevators = int(request.data.get('num_elevators', 0))
        elevators = []
        for i in range(num_elevators):
            elevator = Elevator.objects.create()
            elevators.append(elevator)

        serializer = ElevatorSerializer(elevators, many=True)
        return Response(serializer.data, status=201)


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def list(self, request):
        elevator_id = request.query_params.get('elevator_id')
        queryset = Request.objects.filter(elevator_id=elevator_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
