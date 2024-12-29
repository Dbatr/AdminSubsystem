from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from canban.models import *
from django.shortcuts import get_object_or_404


@extend_schema(
    tags=["Grades"],
    responses=GradeSerializer(many=True)
)
@api_view(['GET'])
def get_all_grades(request):
    """
    Получение всех оценок.
    """
    grades = Grade.objects.all()
    serializer = GradeSerializer(grades, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Grades"],
    responses=GradeSerializer
)
@api_view(['GET'])
def get_grade_by_id(request, grade_id):
    """
    Получение конкретной оценки по ID.
    """
    grade = get_object_or_404(Grade, id=grade_id)
    serializer = GradeSerializer(grade)
    return Response(serializer.data)


@extend_schema(
    tags=["Grades"],
    request=GradeSerializer,
    responses={201: GradeSerializer, 400: "Invalid data"}
)
@api_view(['POST'])
def create_grade(request):
    """
    Создание новой оценки.
    """
    serializer = GradeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Grades"],
    request=GradeSerializer,
    responses={200: GradeSerializer, 400: "Invalid data", 404: "Not Found"}
)
@api_view(['PUT'])
def update_grade(request, grade_id):
    """
    Обновление существующей оценки.
    """
    grade = get_object_or_404(Grade, id=grade_id)
    serializer = GradeSerializer(grade, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Grades"],
    responses={204: "No Content", 404: "Not Found"}
)
@api_view(['DELETE'])
def delete_grade(request, grade_id):
    """
    Удаление оценки.
    """
    grade = get_object_or_404(Grade, id=grade_id)
    grade.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)