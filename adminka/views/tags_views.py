from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from canban.models import *
from django.shortcuts import get_object_or_404


@extend_schema(
    tags=["Tags"],
    responses=TagSerializer(many=True)
)
@api_view(['GET'])
def get_all_tags(request):
    """
    Получение всех тегов.
    """
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Tags"],
    responses=TagSerializer(many=True)
)
@api_view(['GET'])
def get_tags_by_task(request, task_id):
    """
    Получение всех тегов для конкретной задачи.
    """
    task = get_object_or_404(Task, id=task_id)
    tags = Tag.objects.filter(task=task)
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Tags"],
    request=TagSerializer,
    responses={201: TagSerializer, 400: "Invalid data"}
)
@api_view(['POST'])
def create_tag(request):
    """
    Создание нового тега.
    """
    serializer = TagSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Tags"],
    request=TagSerializer,
    responses={200: TagSerializer, 400: "Invalid data", 404: "Not Found"}
)
@api_view(['PUT'])
def update_tag(request, tag_id):
    """
    Обновление существующего тега.
    """
    tag = get_object_or_404(Tag, id=tag_id)
    serializer = TagSerializer(tag, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Tags"],
    responses={204: "No Content", 404: "Not Found"}
)
@api_view(['DELETE'])
def delete_tag(request, tag_id):
    """
    Удаление тега.
    """
    tag = get_object_or_404(Tag, id=tag_id)
    tag.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Tags"],
    responses=TaskSerializer(many=True),
    request=None
)
@api_view(['GET'])
def get_tasks_by_tag_name(request, tag_name):
    """
    Получение всех задач по названию тега.
    """
    tags = Tag.objects.filter(name=tag_name)

    if not tags:
        return Response({"detail": "Tag not found."}, status=status.HTTP_404_NOT_FOUND)

    tasks = Task.objects.filter(tag__in=tags)
    serializer = TaskSerializer(tasks, many=True)

    return Response(serializer.data)
