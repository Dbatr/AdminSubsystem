from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from canban.models import *
from django.shortcuts import get_object_or_404


@extend_schema(
    tags=["Comments"],
    responses=CommentSerializer(many=True)
)
@api_view(['GET'])
def get_all_comments(request):
    """
    Получение всех комментариев.
    """
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Comments"],
    responses=CommentSerializer(many=True)
)
@api_view(['GET'])
def get_comments_by_task(request, task_id):
    """
    Получение комментариев по задаче.
    """
    comments = Comment.objects.filter(task_id=task_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Comments"],
    request=CommentSerializer,
    responses={201: CommentSerializer, 400: "Invalid data"}
)
@api_view(['POST'])
def create_comment(request):
    """
    Создание нового комментария.
    """
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Comments"],
    request=CommentSerializer,
    responses={200: CommentSerializer, 400: "Invalid data", 404: "Not Found"}
)
@api_view(['PUT'])
def update_comment(request, comment_id):
    """
    Обновление существующего комментария.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Comments"],
    responses={204: "No Content", 404: "Not Found"}
)
@api_view(['DELETE'])
def delete_comment(request, comment_id):
    """
    Удаление комментария.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)