from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from canban.models import *
from django.shortcuts import get_object_or_404


@extend_schema(
    tags=["Checklist items"],
    description="Получение всех элементов чек-листов без привязки к конкретной задаче.",
)
@api_view(['GET'])
def get_all_checklist_items_global(request):
    """
    Получение всех элементов чек-листов без привязки к конкретной задаче.
    """
    checklist_items = ChecklistItem.objects.all()
    serializer = ChecklistItemSerializer(checklist_items, many=True)
    return Response(serializer.data)

@extend_schema(
    tags=["Checklist items"],
    description="Получение всех элементов чек-листа для конкретной задачи."
)
@api_view(['GET'])
def get_all_checklist_items(request, task_id):
    """
    Получение всех элементов чек-листа для конкретной задачи.
    """
    checklist_items = ChecklistItem.objects.filter(task_id=task_id)
    serializer = ChecklistItemSerializer(checklist_items, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Checklist items"],
    responses={200: ChecklistItemSerializer, 404: 'Checklist item not found'},
    description="Получение элемента чек-листа по ID."
)
@api_view(['GET'])
def get_checklist_item_by_id(request, task_id, item_id):
    """
    Получение элемента чек-листа по ID.
    """
    checklist_item = get_object_or_404(ChecklistItem, task_id=task_id, id=item_id)
    serializer = ChecklistItemSerializer(checklist_item)
    return Response(serializer.data)


@extend_schema(
    tags=["Checklist items"],
    request=ChecklistItemSerializer,
    responses={201: ChecklistItemSerializer, 400: 'Invalid data'},
    description="Создание нового элемента чек-листа для задачи."
)
@api_view(['POST'])
def create_checklist_item(request, task_id):
    """
    Создание нового элемента чек-листа для задачи.
    """
    data = request.data
    data['task'] = task_id  # Указываем задачу, к которой привязан чек-лист
    serializer = ChecklistItemSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Checklist items"],
    request=ChecklistItemSerializer,
    responses={200: ChecklistItemSerializer, 400: 'Invalid data', 404: 'Checklist item not found'},
    description="Обновление элемента чек-листа."
)
@api_view(['PUT'])
def update_checklist_item(request, task_id, item_id):
    """
    Обновление элемента чек-листа.
    """
    checklist_item = get_object_or_404(ChecklistItem, task_id=task_id, id=item_id)
    serializer = ChecklistItemSerializer(checklist_item, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Checklist items"],
    responses={204: 'No Content', 404: 'Checklist item not found'},
    description="Удаление элемента чек-листа."
)
@api_view(['DELETE'])
def delete_checklist_item(request, task_id, item_id):
    """
    Удаление элемента чек-листа.
    """
    checklist_item = get_object_or_404(ChecklistItem, task_id=task_id, id=item_id)
    checklist_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)