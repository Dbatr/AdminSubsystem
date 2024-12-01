from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from canban.models import *
from django.shortcuts import get_object_or_404

@extend_schema(
    tags=["Tasks"],
)
@api_view(['GET'])
def get_all_tasks(request):
    """
    Получение всех задач.
    """
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Tasks"],
    responses={200: TaskSerializer, 404: 'Task not found'}
)
@api_view(['GET'])
def get_task_by_id(request, task_id):
    """
    Получение задачи по ID.
    """
    task = get_object_or_404(Task, id=task_id)
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@extend_schema(
    tags=["Tasks"],
    request=TaskSerializer,
    responses={201: TaskSerializer, 400: 'Invalid data'}
)
@api_view(['POST'])
def create_task(request):
    """
    Создание новой задачи.
    """
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Tasks"],
    request=TaskSerializer,
    responses={200: TaskSerializer, 400: 'Invalid data', 404: 'Task not found'}
)
@api_view(['PUT'])
def update_task(request, task_id):
    """
    Обновление задачи по ID.
    """
    task = get_object_or_404(Task, id=task_id)
    serializer = TaskSerializer(task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Tasks"],
    responses={204: 'No Content', 404: 'Task not found'}
)
@api_view(['DELETE'])
def delete_task(request, task_id):
    """
    Удаление задачи по ID.
    """
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

