from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from canban.models import *
from django.shortcuts import get_object_or_404


@extend_schema(
    tags=["Results"],
    responses=ResultSerializer(many=True)
)
@api_view(['GET'])
def get_all_results(request):
    """
    Получение всех результатов.
    """
    results = Result.objects.all()
    serializer = ResultSerializer(results, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Results"],
    responses=ResultSerializer
)
@api_view(['GET'])
def get_result_by_id(request, result_id):
    """
    Получение результата по ID.
    """
    result = get_object_or_404(Result, id=result_id)
    serializer = ResultSerializer(result)
    return Response(serializer.data)


@extend_schema(
    tags=["Results"],
    request=ResultSerializer,
    responses={201: ResultSerializer, 400: "Invalid data"}
)
@api_view(['POST'])
def create_result(request):
    """
    Создание нового результата.
    """
    serializer = ResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Results"],
    request=ResultSerializer,
    responses={200: ResultSerializer, 400: "Invalid data", 404: "Not Found"}
)
@api_view(['PUT'])
def update_result(request, result_id):
    """
    Обновление существующего результата.
    """
    result_instance = get_object_or_404(Result, id=result_id)
    serializer = ResultSerializer(result_instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Results"],
    responses={204: "No Content", 404: "Not Found"}
)
@api_view(['DELETE'])
def delete_result(request, result_id):
    """
    Удаление результата.
    """
    result_instance = get_object_or_404(Result, id=result_id)
    result_instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)