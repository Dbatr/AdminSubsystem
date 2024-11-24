from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from crm.models import *
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def get_all_efficiencies(request):
    efficiencies = Efficiency.objects.all()
    serializer = EfficiencySerializer(efficiencies, many=True)
    return Response(serializer.data)


@extend_schema(
    responses={200: EfficiencySerializer, 404: 'Efficiency not found'}
)
@api_view(['GET'])
def get_efficiency_by_user(request, user_id):
    efficiency = get_object_or_404(Efficiency, user_id=user_id)
    serializer = EfficiencySerializer(efficiency)
    return Response(serializer.data)


@extend_schema(
    request=EfficiencySerializer,
    responses={201: EfficiencySerializer, 400: 'Invalid data'}
)
@api_view(['POST'])
def create_efficiency(request):
    serializer = EfficiencySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=EfficiencySerializer,
    responses={200: EfficiencySerializer, 400: 'Invalid data', 404: 'Efficiency not found'}
)
@api_view(['PUT'])
def update_efficiency(request, user_id):
    efficiency = get_object_or_404(Efficiency, user_id=user_id)
    serializer = EfficiencySerializer(efficiency, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=EfficiencySerializer,
    responses={200: EfficiencySerializer, 400: 'Invalid data', 404: 'Efficiency not found'}
)
@api_view(['PATCH'])
def partial_update_efficiency(request, user_id):
    efficiency = get_object_or_404(Efficiency, user_id=user_id)
    serializer = EfficiencySerializer(efficiency, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={204: 'Efficiency deleted', 404: 'Efficiency not found'}
)
@api_view(['DELETE'])
def delete_efficiency(request, user_id):
    efficiency = get_object_or_404(Efficiency, user_id=user_id)
    efficiency.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)