from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from canban.models import *
from django.shortcuts import get_object_or_404


@extend_schema(
    tags=["Customizations"],
    responses=CustomizationSerializer(many=True)
)
@api_view(['GET'])
def get_all_customizations(request):
    """
    Получение всех изображений.
    """
    customizations = Customization.objects.all()
    serializer = CustomizationSerializer(customizations, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Customizations"],
    responses=CustomizationSerializer(many=True)
)
@api_view(['GET'])
def get_customizations_by_task(request, task_id):
    """
    Получение всех изображений для конкретной задачи.
    """
    task = get_object_or_404(Task, id=task_id)
    customizations = Customization.objects.filter(task=task)
    serializer = CustomizationSerializer(customizations, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Customizations"],
    request=CustomizationSerializer,
    responses={201: CustomizationSerializer, 400: "Invalid data"}
)
@api_view(['POST'])
def create_customization(request):
    """
    Создание изображения.
    """
    serializer = CustomizationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Customizations"],
    request=CustomizationSerializer,
    responses={200: CustomizationSerializer, 400: "Invalid data", 404: "Not Found"}
)
@api_view(['PUT'])
def update_customization(request, customization_id):
    """
    Обновление изображения.
    """
    customization = get_object_or_404(Customization, id=customization_id)
    serializer = CustomizationSerializer(customization, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Customizations"],
    responses={204: "No Content", 404: "Not Found"}
)
@api_view(['DELETE'])
def delete_customization(request, customization_id):
    """
    Удаление изображения.
    """
    customization = get_object_or_404(Customization, id=customization_id)
    customization.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)