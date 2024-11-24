from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from crm.models import *
from django.shortcuts import get_object_or_404


@extend_schema(
    responses={200: DirectionSerializer}
)
@api_view(['GET'])
def get_all_directions(request):
    directions = Direction.objects.all()
    serializer = DirectionSerializer(directions, many=True)
    return Response(serializer.data)


@extend_schema(
    responses={200: DirectionSerializer, 404: 'Direction not found'}
)
@api_view(['GET'])
def get_direction_by_id(request, direction_id):
    direction = get_object_or_404(Direction, id=direction_id)
    serializer = DirectionSerializer(direction)
    return Response(serializer.data)


@extend_schema(
    request=DirectionSerializer,
    responses={201: DirectionSerializer, 400: 'Invalid data'}
)
@api_view(['POST'])
def create_direction(request):
    serializer = DirectionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=DirectionSerializer,
    responses={200: DirectionSerializer, 400: 'Invalid data', 404: 'Direction not found'}
)
@api_view(['PUT'])
def update_direction(request, direction_id):
    direction = get_object_or_404(Direction, id=direction_id)
    serializer = DirectionSerializer(direction, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={204: 'No Content', 404: 'Direction not found'}
)
@api_view(['DELETE'])
def delete_direction(request, direction_id):
    direction = get_object_or_404(Direction, id=direction_id)
    direction.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)