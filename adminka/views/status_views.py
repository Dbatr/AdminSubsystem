from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from canban.models import *
from django.shortcuts import get_object_or_404


@extend_schema(
    tags=["Statuses"],
    responses=StatusSerializer(many=True)
)
@api_view(['GET'])
def get_all_statuses(request):
    """
    Получение всех статусов.
    """
    statuses = Status.objects.all()
    serializer = StatusSerializer(statuses, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Statuses"],
    responses=StatusSerializer(many=True)
)
@api_view(['GET'])
def get_statuses_by_direction(request, direction_id):
    """
    Получение всех статусов для конкретного направления.
    """
    direction = get_object_or_404(Direction, id=direction_id)
    statuses = Status.objects.filter(direction=direction)
    serializer = StatusSerializer(statuses, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Statuses"],
    request=StatusSerializer,
    responses={201: StatusSerializer, 400: "Invalid data"}
)
@api_view(['POST'])
def create_status(request):
    """
    Создание нового статуса.
    """
    serializer = StatusSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Statuses"],
    request=StatusSerializer,
    responses={200: StatusSerializer, 400: "Invalid data", 404: "Not Found"}
)
@api_view(['PUT'])
def update_status(request, status_id):
    """
    Обновление существующего статуса.
    """
    status_instance = get_object_or_404(Status, id=status_id)
    serializer = StatusSerializer(status_instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Statuses"],
    responses={204: "No Content", 404: "Not Found"}
)
@api_view(['DELETE'])
def delete_status(request, status_id):
    """
    Удаление статуса.
    """
    status_instance = get_object_or_404(Status, id=status_id)
    status_instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
